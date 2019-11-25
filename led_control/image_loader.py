import os
is_running_on_pi = os.uname()[4][:3] == 'arm'
from PIL import Image

if is_running_on_pi:
    from dotstar import Adafruit_DotStar

rOffset = 3
gOffset = 2
bOffset = 1

class CircularImage:
    def __init__(self, diameter, samples):
        self.diameter = diameter # equal to number of LEDs on strip
        self.samples = samples * 2 # circular resolution / number of samples on the circle

        self.image = [0 for x in range(samples*2)]
        for x in range(samples * 2):
            self.image[x] = bytearray(diameter * 4)
    
    def get_sample(self, index):
        return self.image[index]
    
    # angle between 0 and 1
    def get_sample_by_angle(self, angle):        
        index = int(angle * self.samples)
        return self.get_sample(index)

    def reverse(self):
        self.image.reverse()

class ImageLoader:
    def __init__(self):
        datapin    = 10
        clockpin   = 11

        if is_running_on_pi:
            self.strip = Adafruit_DotStar(0, datapin, clockpin, 18500000)            
        else:
            self.strip = None

    
    def load_to_circular_buffer(self, path):
        if not is_running_on_pi:
            return

        img = Image.open(path).convert("RGB")
        pixels    = img.load()
        width     = img.size[0]
        height    = img.size[1]

        circular_image = CircularImage(height, width)

        bytess = img.tobytes()

        for x in range(width):                        
            offset = x * 3
            multiplier = width * 3
            self.strip.prepareBuffer(circular_image.get_sample(x), bytess, offset, multiplier, False)
        
        for x in range(width):                        
            offset = x * 3
            multiplier = width * 3
            self.strip.prepareBuffer(circular_image.get_sample(x + width), bytess, offset, multiplier, True)

        circular_image.reverse()

        img.close()

        return circular_image
    
    @staticmethod
    def black():
        black = bytearray(144 * 4)
        for x in range(len(black)):
            if x % 4 == 0:
                black[x] = 0xFF
            else:
                black[x] = 0

        return black



if __name__ == "__main__":
    loader = ImageLoader()
    loader.load_to_circular_buffer("incoming_images/shburit/fan_1/Layer 2000.png")