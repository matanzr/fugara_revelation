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

gamma = bytearray(256)
for i in range(256):
	gamma[i] = int(pow(float(i) / 255.0, 2.7) * 255.0 + 0.5)


class UtilityFan:
    def __init__(self):
        datapin    = 10
        clockpin   = 11

        self.buffer = bytearray(STRIP_LENGTH * 4)        
        self.buffer_clear = bytearray(STRIP_LENGTH * 4)        
        self.color_hsv = [0, 1, 0.7]
        self.start_time = time.time()

        self.cur_trail = 0

        for i in range(0, len(self.buffer_clear), 4):     
            self.buffer_clear[i]     = 0xFF
            self.buffer_clear[i + rOffset] = 0
            self.buffer_clear[i + gOffset] = 0
            self.buffer_clear[i + bOffset] = 0

        if is_running_on_pi:
            self.strip = Adafruit_DotStar(0, datapin, clockpin, 18500000)
        else:
            self.strip = None

    def animation_step(self):
        if is_running_on_pi == False:            
            return

        self.color_hsv[0] += 0.002
        color = colorsys.hsv_to_rgb(self.color_hsv[0], self.color_hsv[1], self.color_hsv[2])
        t = time.time() - self.start_time
        
        for i in range(0, len(self.buffer), 4):     
            pos = abs(STRIP_LENGTH/2 - i/4) 
            # v = 0.1* (0.5+ 0.3*math.sin(t*3)) * ((1 + math.sin(i*0.1 + t*11)) + (1 + math.sin(i*0.2 - t*7)) )            
            v = abs(self.cur_trail-pos)/144.0
            self.buffer[i]     = 0xFF
            self.buffer[i + rOffset] = gamma[int(v*255*color[0])] #int(color[0] * v)
            self.buffer[i + gOffset] = gamma[int(v*255*color[1])] #gamma[int(color[1] * v)
            self.buffer[i + bOffset] = gamma[int(v*255*color[2])] #int(color[2] * v)
        
        self.cur_trail = abs(self.cur_trail + 1) % (STRIP_LENGTH)
        self.strip.show(self.buffer)
    
    def next(self, length):         
        end_time = length + time.time()
        last_update = time.time()
        last_frame = time.time()

        self.strip.begin()        
        
        while end_time > last_update:
            last_update = time.time() 
            if last_frame + 0.2 < last_update:
                last_frame = last_update
                self.animation_step()
        
        self.strip.close() 

    def clear(self):
        self.strip.begin()        
        self.strip.show(self.buffer_clear)
        self.strip.close()

if __name__ == "__main__":
    uf = UtilityFan()
    uf.next(10)
    uf.clear()