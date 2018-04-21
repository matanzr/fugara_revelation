import os
is_running_on_pi = os.uname()[4][:3] == 'arm'
from PIL import Image

if is_running_on_pi:
    from dotstar import Adafruit_DotStar
    from magnet_sensor import MagnetButton

import time

rOffset = 3
gOffset = 1
bOffset = 2

STRIP_LENGTH = 144

class PovFan:
    def __init__(self):
        datapin    = 10
        clockpin   = 11

        self.column = None        
        self.width = 0
        
        if is_running_on_pi:
            self.strip = Adafruit_DotStar(0, datapin, clockpin, 12000000)
            self.strip.begin()
        else:
            self.strip = None        
    
    def load_sequence(self, sequence_path):
        img       = Image.open(sequence_path).convert("RGB")
        pixels    = img.load()
        width     = img.size[0]
        height    = img.size[1]

        if (height < STRIP_LENGTH):
            assert("trying to load image too small")

        # Calculate gamma correction table, makes mid-range colors look 'right':
        gamma = bytearray(256)
        for i in range(256):
            gamma[i] = int(pow(float(i) / 255.0, 2.7) * 255.0 + 0.5)

        print( "Allocating...")
        column = [0 for x in range(width)]
        for x in range(width):
            column[x] = bytearray(STRIP_LENGTH * 4)

        print( "Converting...")
        for x in range(width):          # For each column of image...
            for y in range(STRIP_LENGTH): # For each pixel in column...
                value             = pixels[x, y]    # Read pixel in image
                y4                = y * 4           # Position in raw buffer
                column[x][y4]     = 0xFF            # Pixel start marker
                column[x][y4 + rOffset] = int(0.12 * gamma[value[0]]) # Gamma-corrected R
                column[x][y4 + gOffset] = int(0.12 * gamma[value[1]]) # Gamma-corrected G
                column[x][y4 + bOffset] = int(0.12 * gamma[value[2]]) # Gamma-corrected B
        
        self.column = column
        self.width = width
    
    def play(self, length):
        end_time = length + time.time()
        timing = {"lapse_time": 0.2, "last_update": time.time()}

        print "playing sequence for ", length, "seconds"
        if is_running_on_pi:            
            def sync_magnet(counter):
                a = timing
                def magnet_cbk(m):                
                    timing["lapse_time"] = m.estimated_rpm()
                    timing["last_update"] = time.time()
                return magnet_cbk

            magnet = MagnetButton(27)
            magnet.when_magnet = sync_magnet(timing)

            while end_time > timing["last_update"]:
                c = int(self.width * (time.time() - timing["last_update"]) / timing["lapse_time"])
                
                ## if overflowing since lapse is longer now
                if c >= self.width: 
                    c = 0

                self.strip.show(self.column[c])        

        else:
            while end_time > timing["last_update"]: 
                timing["last_update"] = time.time()
    
    def stop():
        pass
    