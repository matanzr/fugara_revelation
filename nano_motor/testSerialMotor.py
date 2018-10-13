import serial
import time

increment = 10

asd = serial.Serial('/dev/ttyUSB0', 9600)
while True:
    speed = int (asd.readline())
    print "reading pmw speed:" + speed

    if speed + increment > 1800 or speed + increment < 1200:
        increment = -increment
    
    asd.write(str(speed+increment))