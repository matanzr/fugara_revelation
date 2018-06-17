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

clients=( rev1.local rev2.local rev3.local rev4.local rev5.local rev6.local rev7.local)

#--- end config

echo to remove password use: ssh-copy-id pi@rev4.local

sync() {
    rsync $FLAGS --exclude='*.png' $FROM $USER@rev1.local:$TO &
    # rsync $FLAGS --exclude='*.png' $FROM $USER@rev2.local:$TO &
    # rsync $FLAGS --exclude='*.png' $FROM $USER@rev3.local:$TO &
    # rsync $FLAGS --exclude='*.png' $FROM $USER@rev4.local:$TO &
    # rsync $FLAGS --exclude='*.png' $FROM $USER@rev5.local:$TO &
    # rsync $FLAGS --exclude='*.png' $FROM $USER@rev6.local:$TO &
    wait

    ssh pi@rev1.local 'cd dev/fugara_revelation && python firebase_sync.py extract' &
    # ssh pi@rev2.local 'cd dev/fugara_revelation && python firebase_sync.py extract' &
    # ssh pi@rev3.local 'cd dev/fugara_revelation && python firebase_sync.py extract' &
    # ssh pi@rev4.local 'cd dev/fugara_revelation && python firebase_sync.py extract' &
    # ssh pi@rev5.local 'cd dev/fugara_revelation && python firebase_sync.py extract' &
    # ssh pi@rev6.local 'cd dev/fugara_revelation && python firebase_sync.py extract' & 
    wait
}

stop() {
    ssh pi@rev1.local 'sudo pkill -f python'
}

start() {
    ssh pi@rev1.local './launcher/launcher.sh'
}

git_pull() {
    ssh $USER@$1 'cd dev/fugara_revelation/led_control && make' &
}

reboot() {
    ssh $1 'sudo reboot' &
}

make() {
    ssh $USER@$1 'cd dev/fugara_revelation/led_control && make' &
}

ping() {
    ping -c 1 -W 1 rev1.local
    # if [ $? -eq 0 ]
    # then
    #     echo $1 "Pingable"
    # else
    #     echo $1 "Not Pingable"
    # fi
    
    # ping -c 1 -W 1 rev1.local ; echo $? & 
    # ping -c 1 -W 1 rev2.local ; echo $? &
    # ping -c 1 -W 1 rev3.local ; echo $? &
    # ping -c 1 -W 1 rev4.local ; echo $? &
    # ping -c 1 -W 1 rev5.local ; echo $? &
    # ping -c 1 -W 1 rev6.local ; echo $? &
}
sync
# if declare -f "$1" > /dev/null
# then
#   # call arguments verbatim
#   for i in "${clients[@]}"
#     do
#         "$@" $i  
#     done
#     wait


# else
#   # Show a helpful error
#   echo "'$1' is not a known function name" >&2
#   echo "Options: make, reboot, git_pull, sync, ping"
#   exit 1
# fi

