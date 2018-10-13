import serial
import time

increment = 20

asd = serial.Serial('/dev/ttyUSB0', 9600)

time.sleep(3)
print asd.write('1\r\n')
# asd.flush()

speed = int(asd.readline())
print "reading pmw speed:" + str(speed)     

print asd.write('1800\r\n')

time.sleep(5)

print asd.write('1200\r\n')

time.sleep(5)

print asd.write('1800\r\n')

print asd.write('1\r\n')
asd.flush()
speed = int(asd.readline())
print "reading pmw? speed:" + str(speed)     
print speed           