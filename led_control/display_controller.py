import time
from magnet_sensor import MagnetButton

MAX_LAPSE_TIME = 0.33
INIT_LAPSE_TIME = 0.18
NO_MAGNET_LAPSE_TIME = 0.2
MAGNET_PIN = 16

class DisplayController:
    def __init__(self):
        self.lapse_time = INIT_LAPSE_TIME
        self.last_update = time.time()
        self.lapses = 0

        self.max_lapse_time = MAX_LAPSE_TIME   # max time allowed before force swap
        self.use_magnet = True

        self.magnet = MagnetButton(MAGNET_PIN)
        self.magnet.when_magnet = self.sync_magnet()
        self.magnet.set_timeout(self.max_lapse_time)
    
    def sync_magnet(self):
        def magnet_cbk(m):                                                
            if not self.use_magnet: 
                return
            
            self.lapse_time = m.estimated_rpm()
            self.last_update = time.time()
            self.lapses = self.lapses + 1

        return magnet_cbk

    def no_magnet_callback(self):
        self.lapse_time = NO_MAGNET_LAPSE_TIME
        self.last_update = time.time()
        self.lapses = self.lapses + 1

        if self.lapses % 10 == 0:
            print "MAGNET SENSOR INACTIVE! FALLBACK ESTIMATING SPEED"

    def update(self):
        self.use_magnet = not (self.magnet.is_not_responding())

        if not self.use_magnet and time.time() - self.last_update > self.max_lapse_time:
            self.no_magnet_callback()
    
    def estimate_angle(self):
        angle = (time.time() - self.last_update) / self.lapse_time
        return angle % 1 # return angle in range of 0-1

    def close(self):
        self.magnet.close()


if __name__ == "__main__":
    from motor_controller import MotorController
    mc = MotorController()

    mc.connect()
    mc.set_motor_speed(1650)
    mc.sync_speed(5)

    display_c = DisplayController()
    end_time = 5 + time.time()

    while end_time > display_c.last_update:
        display_c.update()
        time.sleep(0.0001)
    
    display_c.close()