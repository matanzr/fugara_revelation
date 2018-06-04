# Fugara Revelation

## Installation:

### Set up the Raspberry PI zero w:

 - Get Raspbian lite from here:
https://www.raspberrypi.org/downloads/raspbian/

- Set up wifi:
Edit `wpa_supplicat.conf` (version attached in this repo) to match your wifi, then copy it to the boot sdcrad you made in last step.

- Enable spi: 
Edit config.txt on sdcard - uncomment `dtparam=spi=on`

- Connecting to PI over ssh
    - To enable ssh, put an empty `ssh` file on the sdcard
    - ssh to pi: `ssh pi@raspberrypi.local` should work. otherwise try to figure out ip manually.

- Set pi hostname:
    - `sudo nano /etc/hosts` and change last line from raspberry to rev{number}
    - `sudo nano /etc/hostname` and change to same rev{number}
    - `sudo reboot`
    - now ssh with new name: `ssh pi@rev{number}.local`

- Install packages 
    - `sudo apt-get update`
    - `sudo apt-get install build-essential python-pip python-dev python-smbus git python-gpiozero libopenjp2-7-dev libtiff5-dev`

    - (optional) Prepare GIT: `git config --global user.name "John Doe" && git config --global user.email johndoe@example.com`
    
    - `mkdir dev && cd dev`
    - Fetch the Adafruit_Python_GPIO library: 
        ```
        git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
        cd Adafruit_Python_GPIO
        sudo python setup.py install
        ```

- Setup led control
    - `cd ~/dev && git clone https://github.com/matanzr/fugara_revelation.git`
    - `cd ~/dev/fugara_revelation/led_control`
    - `make`
    -  Install pillow: `pip install Pillow`

- Setup script service
    - `pip install pyrebase`
    - `pip install firebase_admin`

## Perparing Content

- Image converter to Radial format
https://matanzr.github.io/fugara_revelation/image_converter/ImageConvertRadial.html
