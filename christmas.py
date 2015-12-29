from sense_hat import SenseHat
import time

sh=SenseHat()

FRAMES = [
[[0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [255, 0, 0], [0, 0, 0], [255, 255, 255], [0, 0, 0], [255, 0, 0], [0, 0, 0], [255, 255, 255], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 128, 0], [255, 128, 0], [255, 128, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 128, 0], [255, 128, 0], [255, 128, 0], [0, 0, 255], [0, 0, 255], [255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 128, 0], [255, 128, 0], [255, 128, 0], [0, 0, 255], [0, 0, 255]],
[[0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [255, 255, 255], [0, 0, 0], [255, 0, 0], [0, 0, 0], [255, 255, 255], [0, 0, 0], [255, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 128, 0], [255, 128, 0], [255, 128, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 128, 0], [255, 128, 0], [255, 128, 0], [0, 0, 255], [0, 0, 255], [255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 128, 0], [255, 128, 0], [255, 128, 0], [0, 0, 255], [0, 0, 255]],
]

while True:
    for x in FRAMES:
        sh.set_pixels(x)
        time.sleep(0.5)