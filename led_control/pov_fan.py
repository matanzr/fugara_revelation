import os
import glob
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

        self.images_folder = ""

        if is_running_on_pi:
            self.strip = Adafruit_DotStar(0, datapin, clockpin, 18500000)            
        else:
            self.strip = None

    def add_image(self, image_path, reverse):
        if is_running_on_pi == False:
            # print "add_image"
            return
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
            self.strip.prepareBuffer(column[x], bytess, offset, multiplier, reverse)

        self.sequence.append(column)
        self.width = width

        img.close()

    def disabled_animation(): pass
    
    def clear_fan(): pass

    def loading_animation(): pass

    #TODO: set sequence length
    def load_sequence(self, sequence_path, fan_id, seq_size = -1):
        if is_running_on_pi == False:
            # print "load_sequence: ", sequence_path, fan_id
            return
        start = time.time()
        path = os.path.join(self.images_folder, 'incoming_images', sequence_path, "fan_"+str(fan_id))
        files = sorted( glob.glob( os.path.join(path, "*.png") ))
        
        for i in range(len(files)):
            print "loading image ", i
            self.add_image(files[i], i%2)

        print "loading took ", time.time() - start

    def next_image(self, magnet_synced=False):
        self.cur_column = (self.cur_column + 1) % len(self.sequence)
        
        # Make sure that is on even numbered image when hitting magnet
        if magnet_synced and self.cur_column % 2 == 1:
            self.cur_column = (self.cur_column + 1) % len(self.sequence)
            
        self.column = self.sequence[self.cur_column]
        print "showing frame #",self.cur_column

    def no_magnet_callback(self, timing):
        timing["lapse_time"] = timing["no_magnet_lapse_time"]
        timing["last_update"] = time.time()
        timing["lapses"] = timing["lapses"] + 1
        timing["need_swap"] = 0
        if timing["lapses"] % 10 == 0:
            print "MAGNET SENSOR INACTIVE! FALLBACK ESTIMATING SPEED"
            print "lapse ", timing["lapses"], " refresh count: ", timing["refresh_count"]
            print "lapse time", timing["lapse_time"]
            timing["refresh_count"] = 0

    def play(self, length):
        if len(self.sequence) == 0:
            print "No sequence loaded! Cancel play"
            return
        
        if is_running_on_pi == False:            
            return

        self.strip.begin()

        end_time = length + time.time()
        PIXELS_IN_CIRCLE = 2 * self.width
        self.column = self.sequence[self.cur_column]        

        timing = {
            "lapse_time": 0.18,             # time to complete lapse
            "last_update": time.time(),     # last frame time
            "lapses": 0,                    # number of whole rotations (or every magnet on)
            "refresh_count": 0,             # number of columns showed
            "need_swap": 0,                 # track for estimating mid-lapse image swap
            "max_lapse_time": 0.21,          # max time allowed before force swap
            "use_magnet": True,
            "no_magnet_lapse_time": 0.3
            }

        print "playing sequence for ", length, "seconds"
        if is_running_on_pi:
            def sync_magnet(counter):
                a = timing

                def magnet_cbk(m):                    
                    if not timing["use_magnet"]: 
                        return

                    timing["lapse_time"] = m.estimated_rpm()
                    timing["last_update"] = time.time()
                    timing["lapses"] = timing["lapses"] + 1
                    timing["need_swap"] = 0
                    if timing["lapses"] % 10 == 0:
                        print "lapse ", timing["lapses"], " refresh count: ", timing["refresh_count"]
                        print "lapse time", timing["lapse_time"]
                        timing["refresh_count"] = 0
                return magnet_cbk

            magnet = MagnetButton(16)
            magnet.when_magnet = sync_magnet(timing)
            magnet.set_timeout(timing["max_lapse_time"])

            while end_time > timing["last_update"]:
                timing["use_magnet"] = not (magnet.is_not_responding())

                if not timing["use_magnet"]:
                    if time.time() > timing["last_update"] + timing["no_magnet_lapse_time"]:
                        self.no_magnet_callback(timing)
            
                if timing["need_swap"] == 0:
                    self.next_image()
                    timing["need_swap"] = 1

                c = int(PIXELS_IN_CIRCLE * (time.time() - timing["last_update"]) / timing["lapse_time"])

                # TODO: make this cleaner...
                if c >= (self.width):
                    if timing["need_swap"] == 1:
                        self.next_image()
                        timing["need_swap"] = 2

                    ## if overflowing since lapse is longer now
                    c = c % self.width                    

                self.strip.show(self.column[c])
                timing["refresh_count"] = timing["refresh_count"] + 1

            magnet.close()

        else:
            while end_time > timing["last_update"]:
                timing["last_update"] = time.time()
        
        self.strip.close()

    def stop(self):
        self.strip.clear()
        self.strip.close()

if __name__ == "__main__":
    while 1:
        fan = PovFan()
        fan.load_sequence("senses", 1)
        fan.play(60)
