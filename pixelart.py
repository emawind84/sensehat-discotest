#!/usr/bin/env python
# coding: utf-8
from sense_hat import SenseHat
import time, os
from PIL import Image

sense = SenseHat()

def showImage():

    image_file = os.path.join(os.sep, "/home", "pi", "python_example/sensehat", "pixelart_sample2.gif")
    img = Image.open(image_file)

    rgb_img = img.convert('RGB')
    image_pixels = list(rgb_img.getdata())

    #print(image_pixels)
    pixel_width = 6
    image_width = pixel_width * 8
    sense_pixels = []
    start_pixel = 0
    while start_pixel < (image_width * 64):
        sense_pixels.extend(image_pixels[start_pixel:(start_pixel+image_width):pixel_width])
        start_pixel += (image_width * pixel_width)

    print(sense_pixels)
    sense.set_pixels(sense_pixels)

def main():
    try:
        showImage()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    main()
