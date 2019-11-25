import os
import glob
import time
is_running_on_pi = os.uname()[4][:3] == 'arm'

if is_running_on_pi:
    from dotstar import Adafruit_DotStar
    from image_loader import ImageLoader
    from display_controller import DisplayController

STRIP_LENGTH = 144
LED_BRIGHTNESS = 0.7
PHYSICAL_ANGLE_OFFSET = 100

class PovFan:
    def __init__(self):
        datapin    = 10
        clockpin   = 11

        self.column = None
        self.width = 0
        self.sequence = []
        self.cur_column = 0

        self.start_time = 0
        self.fps = 16

        self.images_folder = ""

        if is_running_on_pi:
            self.strip = Adafruit_DotStar(0, datapin, clockpin, 18500000)            
        else:
            self.strip = None

    def disabled_animation(): pass
    
    def clear_fan(): pass

    def loading_animation(): pass

    #TODO: set sequence length
    def load_sequence(self, sequence_path, fan_id, seq_size = -1):        
        if is_running_on_pi == False:
            return

        start = time.time()

        image_loader = ImageLoader()
        path = os.path.join(self.images_folder, 'incoming_images', sequence_path, "fan_"+str(fan_id))
        files = sorted( glob.glob( os.path.join(path, "*.png") ))
        
        for i in range(len(files)):
            circular_image = image_loader.load_to_circular_buffer(files[i])
            if (circular_image.diameter < STRIP_LENGTH):
                assert("load_sequence(): trying to load image too small for strip length")
            self.sequence.append(circular_image)

        print ("Successfuly loaded ", len(files))
        print ("loading took ", time.time() - start)

    def get_frame(self):
        seq_length = len(self.sequence)
        elapsed_time = time.time() - self.start_time
        frame = int(elapsed_time * self.fps) % seq_length

        return self.sequence[frame]

    def play(self, length, display_controller):        
        if len(self.sequence) == 0:
            print ("No sequence loaded! Cancel play")
            return
        
        if is_running_on_pi == False:            
            return

        if display_controller is None:
            display_controller = DisplayController()

        self.strip.begin()
        self.start_time = time.time()
        end_time = length + self.start_time        

        black = ImageLoader.black()
        # angle_offset_pixels = (int) (PHYSICAL_ANGLE_OFFSET * 360.0 / PIXELS_IN_CIRCLE)
        # print "offsting image by " + str(angle_offset_pixels) 
        print ("playing sequence for ", length, "seconds")

        current_image = self.sequence[0]
        counter = 0

        last_switch = time.time()
        diff = 0
        if is_running_on_pi:
            while end_time > display_controller.last_update:
                diff = diff + time.time() - last_switch
                last_switch = time.time()

                current_image = self.get_frame()
                display_controller.update()
                angle = display_controller.estimate_angle()
                
                self.strip.show(current_image.get_sample_by_angle(angle))
                time.sleep(0.0001) 

        else:
            while end_time > timing["last_update"]:
                timing["last_update"] = time.time()
        
        
        self.stop()
        # self.strip.show(bytearray(STRIP_LENGTH * 4))

        # self.strip.close()

    def stop(self):
        self.strip.show(ImageLoader.black())
        self.strip.close()

if __name__ == "__main__":
    from motor_controller import MotorController
    mc = MotorController()

    mc.connect()
    mc.set_motor_speed(1700)
    mc.sync_speed(5)

    display_controller = DisplayController()    
    fan = PovFan()
    fan.load_sequence("KfirRam", 1)
    # fan.load_sequence("shburit", 1)
    fan.play(10, display_controller)
    display_controller.close()

    # mc.set_motor_speed(1600)
    # mc = MotorController()
    # mc.connect()
