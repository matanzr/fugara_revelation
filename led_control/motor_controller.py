import serial
import time
from magnet_sensor import MagnetButton

STOP_SPEED = 1500

class MotorController:
    def __init__(self):
        self.asd = None
        self.speed = STOP_SPEED

    def connect(self):
        self.asd = serial.Serial('/dev/ttyUSB0', 9600)
        time.sleep(3)
        print "Connected to motor"


    def set_motor_speed(self, speed):
        if self.asd is None:
            print "Not connected to motor"
            return

        if speed < 1300 or speed > 1800:
            print "use speeds between 1300 and 1800"
            return
        
        self.asd.write(str(speed) + '\r\n')
        self.speed = speed

        time.sleep(2)

    def stop_motor(self):
        self.set_motor_speed(STOP_SPEED)    

    def sync_speed(self, target_frequency):
        with MagnetButton(16) as button:
            lapse_time = 1.0/float(target_frequency)
            print "attempting to find speed for target lapse time " + str(lapse_time)

            n = 0
            last_step = 0
            increment = 20

            while True:
                if abs(button.estimated_rpm() - lapse_time) < 0.005:
                    print "close enough.... gooddday"
                    return 

                print "using speed increment: " + str(increment)
                if button.estimated_rpm() > lapse_time:
                    self.set_motor_speed(self.speed + increment)
                    if last_step == -1:
                        increment = int(increment / 2)

                    last_step = 1
                
                if button.estimated_rpm() < lapse_time:
                    self.set_motor_speed(self.speed - increment)
                    if last_step == 1:
                        increment = int(increment / 2)

                    last_step = -1

                n = n+1            
                print button.estimated_rpm()                        

                # time.sleep(0.3)
        



if __name__ == "__main__":
    mc = MotorController()

    mc.connect()
    mc.set_motor_speed(1700)
    mc.sync_speed(5)

    n = 5
    button = MagnetButton(16)
    while n > 0:
        n = n - 1
        print button.estimated_rpm()
        time.sleep(1.5)

    mc.stop_motor()