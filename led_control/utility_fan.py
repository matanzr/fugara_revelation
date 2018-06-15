import os
import colorsys
import math
import random

is_running_on_pi = os.uname()[4][:3] == 'arm'

if is_running_on_pi:
    from dotstar import Adafruit_DotStar

import time

rOffset = 3
gOffset = 2
bOffset = 1

STRIP_LENGTH = 144

class UtilityFan:
    def __init__(self):
        datapin    = 10
        clockpin   = 11

        self.buffer = bytearray(STRIP_LENGTH * 4)        
        self.color_hsv = [0, 1, 0.7]
        self.start_time = time.time()

        if is_running_on_pi:
            self.strip = Adafruit_DotStar(0, datapin, clockpin, 18500000)
        else:
            self.strip = None

    def animation_step(self):
        if is_running_on_pi == False:            
            return

        self.color_hsv[0] += 0.001
        color = colorsys.hsv_to_rgb(self.color_hsv[0], self.color_hsv[1], self.color_hsv[2])
        t = time.time() - self.start_time
        
        for i in range(0, len(self.buffer), 4):     
            v = 0.1* (0.5+ 0.3*math.sin(t*3)) * ((1 + math.sin(i*0.1 + t*11)) + (1 + math.sin(i*0.2 - t*7)) )            

            self.buffer[i]     = 0xFF
            self.buffer[i + rOffset] = int(v*255*color[0]) #int(color[0] * v)
            self.buffer[i + gOffset] = int(v*255*color[1]) #int(color[1] * v)
            self.buffer[i + bOffset] = int(v*255*color[2]) #int(color[2] * v)
        
        self.strip.show(self.buffer)
    
    def next(self, length): 
        end_time = length + time.time()
        last_update = time.time()

        self.strip.begin()        
        
        while end_time > last_update:
            last_update = time.time()
            self.animation_step()
        
        self.strip.close()

if __name__ == "__main__":
    uf = UtilityFan()

    
    uf.next(10)