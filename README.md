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
    - Install Git: `sudo apt-get install git`
    - Prepare GIT: `git config --global user.name "John Doe" && git config --global user.email johndoe@example.com`
    -  Install Python 3 and some packages required by the Adafruit library: `sudo apt-get install -y python3 python3-dev python3-pip python3-smbus python3-rpi.gpio build-essential`
    - `sudo apt-get install build-essential python-pip python-dev python-smbus git`
    - `mkdir dev && cd dev`
    - Fetch the Adafruit_Python_GPIO library: `git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
    cd Adafruit_Python_GPIO`
    - `sudo python3 setup.py install`
    - (Test if everything works so far by running https://github.com/tinue/APA102_Pi)
    
    - `cd ~/dev && git clone https://github.com/adafruit/Adafruit_DotStar_Pi`
    - `cd Adafruit_DotStar_Pi/`
    - Install pillow: `pip3 install Pillow`
    - `sudo apt-get install libopenjp2-7-dev`
    - `sudo apt-get install libtiff5-dev`

## Perparing Content

- Image converter to Radial format
https://matanzr.github.io/fugara_revelation/image_converter/ImageConvertRadial.html