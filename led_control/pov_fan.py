import os
is_running_on_pi = os.uname()[4][:3] == 'arm'
from PIL import Image

if is_running_on_pi:
    from dotstar import Adafruit_DotStar
    from magnet_sensor import MagnetButton

import time

rOffset = 3
gOffset = 2
bOffset = 1

STRIP_LENGTH = 144

LED_BRIGHTNESS = 0.7

class PovFan:
    def __init__(self):
        datapin    = 10
        clockpin   = 11

        self.column = None        
        self.width = 0
        self.sequence = []
        self.cur_column = 0
        
        if is_running_on_pi:
            self.strip = Adafruit_DotStar(0, datapin, clockpin, 18500000)
            self.strip.begin()
        else:
            self.strip = None        
    
    def add_image(self, image_path):
        img       = Image.open(image_path).convert("RGB")
        pixels    = img.load()
        width     = img.size[0]
        height    = img.size[1]

        if (height < STRIP_LENGTH):
            assert("trying to load image too small")

        
        column = [0 for x in range(width)]
        for x in range(width):
            column[x] = bytearray(STRIP_LENGTH * 4)        
        
        bytess = img.tobytes()
        
        for x in range(width): 
            offset = x * 3
            multiplier = width * 3
            self.strip.prepareBuffer(column[x], bytess, offset, multiplier);
        
        
        # Calculate gamma correction table, makes mid-range colors look 'right':
        # gamma = bytearray(256)
        # for i in range(256):
        #     gamma[i] = int(pow(float(i) / 255.0, 2.7) * 255.0 + 0.5)

        # print( "Converting...")
        # for x in range(width):          # For each column of image...
        #     for y in range(STRIP_LENGTH): # For each pixel in column...
        #         value             = pixels[x, y]    # Read pixel in image
        #         y4                = y * 4           # Position in raw buffer                
        #         if column[x][y4] != 0xFF: assert("not even")
        #         if column[x][y4 + rOffset] != int(gamma[value[0]]): print column[x][y4 + rOffset], int(gamma[value[0]])
        #         if column[x][y4 + gOffset] != int(gamma[value[1]]): print meh
        #         if column[x][y4 + bOffset] != int(gamma[value[2]]): print meh
        #         # column[x][y4]     = 0xFF            # Pixel start marker
        #         # column[x][y4 + rOffset] = int(LED_BRIGHTNESS * gamma[value[0]]) # Gamma-corrected R
        #         # column[x][y4 + gOffset] = int(LED_BRIGHTNESS * gamma[value[1]]) # Gamma-corrected G
        #         # column[x][y4 + bOffset] = int(LED_BRIGHTNESS * gamma[value[2]]) # Gamma-corrected B
        
             
        self.sequence.append(column)
        self.width = width

        img.close()

    #TODO: set sequence length
    def load_sequence(self, sequence_path, seq_size = 1):                        
        # self.add_image("./test_images/test_skull.png")
        # self.add_image("./viceland/viceland050.png")
        start = time.time()
        for i in range(seq_size):
            #viceland/viceland000.png
            print "loading image ", i , " from sequnce: ", "cube" + str(0+i).zfill(3) + ".png"
            # self.add_image(os.path.join(sequence_path, "cube" + str(0+i).zfill(3) + ".png"))
            # print "loading image ", i , " from sequnce: ", "viceland" + str(150+i).zfill(3) + ".png"
            self.add_image(os.path.join(sequence_path, "viceland" + str(0+i).zfill(3) + ".png"))
        
        print "loading took ", time.time() - start
    
    def next_image(self):
        self.cur_column = (self.cur_column + 1) % len(self.sequence)
        self.column = self.sequence[self.cur_column]
        print "showing frame #",self.cur_column
    
    def play(self, length):
        end_time = length + time.time()
        self.column = self.sequence[self.cur_column]

        timing = {"lapse_time": 0.2, "last_update": time.time(), "lapses": 0, "refresh_count": 0, "need_swap": 0}        

        print "playing sequence for ", length, "seconds"
        if is_running_on_pi:            
            def sync_magnet(counter):
                a = timing

                def magnet_cbk(m):                
                    timing["lapse_time"] = m.estimated_rpm()
                    timing["last_update"] = time.time()
                    timing["lapses"] = timing["lapses"] + 1
                    timing["need_swap"] = 0
                    if timing["lapses"] % 5 == 0:
                        print "lapse ", timing["lapses"], " refresh count: ", timing["refresh_count"]
                        print "lapse time", timing["lapse_time"] 
                        timing["refresh_count"] = 0
                return magnet_cbk

            magnet = MagnetButton(27)
            magnet.when_magnet = sync_magnet(timing)

            while end_time > timing["last_update"]:
                if timing["need_swap"] == 0: 
                    self.next_image()
                    timing["need_swap"] = 1

                c = int(self.width * (time.time() - timing["last_update"]) / timing["lapse_time"])
                
                # TODO: make this cleaner...
                if c >= (self.width / 2):
                    if timing["need_swap"] == 1:
                        self.next_image()
                        timing["need_swap"] = 2
                    
                    ## if overflowing since lapse is longer now
                    if c >= self.width:                     
                        c = 0
                    
                    # TODO: This should run when sensor isn't responding...     
                    timing["last_update"] = time.time() 
                    timing["lapses"] = timing["lapses"] + 1
                    self.next_image()
                    if timing["lapses"] % 5 == 0:
                        print "(speed sensor off) lapse ", timing["lapses"], " refresh count: ", timing["refresh_count"]
                        timing["refresh_count"] = 0

                self.strip.show(self.column[c])    
                timing["refresh_count"] = timing["refresh_count"] + 1

            magnet.close()    

        else:
            while end_time > timing["last_update"]: 
                timing["last_update"] = time.time()
    
    def stop():
        pass

if __name__ == "__main__":
    fan = PovFan()
    fan.load_sequence("./viceland/", 200)
    fan.play(200)