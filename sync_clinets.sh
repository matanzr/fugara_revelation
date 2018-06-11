#!/bin/bash
#-- start config
# Local Directory for backups. A date-specific folder is created under this directory for the files.
FROM=./led_control/incoming_images/
# Remote Directory to retrieve. Files are retrieved recursively starting here. Hidden files are included.
# Must be full path, don't use ~ shortcut.
TO=dev/fugara_revelation/led_control/
# Path to SSH ID file (private key)
ID=~/.ssh/id_rsa
# USERname to login as
USER=pi
FLAGS=-avh --delete

#--- end config

echo to remove password use: ssh-copy-id pi@rev4.local

rsync $FLAGS --exclude='*.png' $FROM $USER@rev1.local:$TO
rsync $FLAGS --exclude='*.png' $FROM $USER@rev2.local:$TO
rsync $FLAGS --exclude='*.png' $FROM $USER@rev3.local:$TO
rsync $FLAGS --exclude='*.png' $FROM $USER@rev4.local:$TO
rsync $FLAGS --exclude='*.png' $FROM $USER@rev5.local:$TO
rsync $FLAGS --exclude='*.png' $FROM $USER@rev6.local:$TO