#!/bin/bash
#-- start config
# Local Directory for backups. A date-specific folder is created under this directory for the files.
LD=./led_control/incoming_images/
# Remote Directory to retrieve. Files are retrieved recursively starting here. Hidden files are included.
# Must be full path, don't use ~ shortcut.
RD=dev/fugara_revelation/led_control/
# Path to SSH ID file (private key)
ID=~/.ssh/id_rsa
# USERname to login as
USER=pi
# HOST to login to
HOST=rev4.local
#--- end config

Echo to remove password use: ssh-copy-id pi@rev4.local
 
scp -r $LD pi@rev1.local:dev/fugara_revelation/led_control/
scp -r $LD pi@rev2.local:dev/fugara_revelation/led_control/
scp -r $LD pi@rev3.local:dev/fugara_revelation/led_control/
scp -r $LD pi@rev4.local:dev/fugara_revelation/led_control/
scp -r $LD pi@rev5.local:dev/fugara_revelation/led_control/
scp -r $LD pi@rev6.local:dev/fugara_revelation/led_control/