# Install rmate on fans
#sudo wget -O /usr/local/bin/rmate https://raw.github.com/aurora/rmate/master/rmate
#sudo chmod a+x /usr/local/bin/rmate

USER=pi

# run fan with ID and Server
fan(){
    echo kill fan $1
    ssh -o ConnectTimeout=1 -q $USER@rev$1.local 'sudo pkill -f python' 

    echo start fan $1 as fan $2 connecting to $3
    ssh -o ConnectTimeout=1 $USER@rev$1.local 'cd /home/pi/dev/fugara_revelation/led_control && export FAN_ID='$2'; export SERVER_IP=http://'$3':3000/; python fan_client.py'

    # cd /home/pi/dev/fugara_revelation/led_control
    # sudo -H -u pi bash -c 'export FAN_ID=3; export SERVER_IP=http://revmaster.local:3000/; python fan_client.py'

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
