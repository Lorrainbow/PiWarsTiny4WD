import explorerhat
from time import sleep
import time
import board
import neopixel
from picamera import PiCamera
camera = PiCamera()

from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageFont

font = ImageFont.load_default()
device = sh1106(port=1, address=0x3C)

#pixels
pixel_pin = board.D18

num_pixels = 10

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def rainbow_cycle(wait):
    print ("rainbow")
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

		
#font = ImageFont.load_default()
font = ImageFont.truetype('sh1106/fonts/C&C Red Alert [INET].ttf', 40)		
		
		
with canvas(device) as draw:
    draw.text((0, 0), 'Lights', font=font, fill=255)
		
pixels.fill((255, 0, 0))
pixels.show()
time.sleep(1)
pixels.fill((0,255, 0))
pixels.show()
time.sleep(1)
rainbow_cycle(0.001)    # rainbow cycle with 1ms delay per step
pixels.fill((0, 0, 0))
time.sleep(1)
pixels.show()
		

with canvas(device) as draw:
    draw.text((0, 0), 'Camera', font=font, fill=255)

camera.start_preview()
sleep(3)
camera.capture('/home/pi/image.jpg')
camera.stop_preview()
	
with canvas(device) as draw:
    draw.text((0, 0), 'Action!', font=font, fill=255)

explorerhat.motor.one.forward(100)
explorerhat.motor.two.forward(100)
sleep(2)
explorerhat.motor.one.stop()
explorerhat.motor.two.stop()