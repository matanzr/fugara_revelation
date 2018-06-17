#!/bin/bash
#-- start config
# Local Directory for backups. A date-specific folder is created under this directory for the files.
FROM=./led_control/incoming_images/
# Remote Directory to retrieve. Files are retrieved recursively starting here. Hidden files are included.
# Must be full path, don't use ~ shortcut.
TO=dev/fugara_revelation/led_control/incoming_images/
# Path to SSH ID file (private key)
ID=~/.ssh/id_rsa
# USERname to login as
USER=pi
FLAGS="-avh --delete"
PATH=~/dev/fugara_revelation 

clients=( rev1.local rev2.local rev3.local rev4.local rev5.local rev6.local rev7.local)

#--- end config

echo to remove password use: ssh-copy-id pi@rev4.local

sync() {
    for i in "${clients[@]}"
    do
        echo rsync $FLAGS --exclude='*.png' $FROM $USER@$1:$TO &
        rsync $FLAGS --exclude='*.png' $FROM $USER@$1:$TO &
    done
    
    wait

    for i in "${clients[@]}"
    do
        echo ssh -o ConnectTimeout=1 -q $USER@$i  'cd $PATH && python firebase_sync.py extract' &
        ssh -o ConnectTimeout=1 -q $USER@$i  'cd $PATH && python firebase_sync.py extract' &
    done

    wait
}

download() {
    cd $PATH && python firebase_sync.py
}

stop() {
    for i in "${clients[@]}"
    do
        echo ssh -o ConnectTimeout=1 -q $USER@$i 'sudo pkill -f python' &
        ssh -o ConnectTimeout=1 -q $USER@$i 'sudo pkill -f python' &
    done
}

start() {
    for i in "${clients[@]}"
    do
        echo ssh -o ConnectTimeout=1 -q $USER@$i './launcher/launcher.sh >/dev/null &' &
        ssh -o ConnectTimeout=1 -q $USER@$i './launcher/launcher.sh >/dev/null &' &
    done
}

git_pull() {
    for i in "${clients[@]}"
    do
        echo ssh $USER@$1 'cd dev/fugara_revelation/led_control && git pull' &
        ssh $USER@$1 'cd dev/fugara_revelation/led_control && git pull' &
    done
}

restart() {
    stop
    wait
    start
}

make() {
    for i in "${clients[@]}"
    do
        ssh $USER@$1 'cd $PATH && make && exit' &
    done
}

ping() {
    for i in "${clients[@]}"
    do
        ping -c 1 -W 1 $1 &
    done
    # if [ $? -eq 0 ]
    # then
    #     echo $1 "Pingable"
    # else
    #     echo $1 "Not Pingable"
    # fi
}

if declare -f "$1" > /dev/null
then
    "$@"

else
  # Show a helpful error
  echo "'$1' is not a known function name" >&2
  echo "Options:"
  "make, reboot, git_pull, sync, ping, start, stop, restart, download"
  exit 1
fi

