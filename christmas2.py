from sense_hat import SenseHat
import time, sys

sh = SenseHat()
sh.low_light = True

FRAMES = [
[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 255, 255], [0, 255, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 255, 0], [0, 255, 0], [255, 255, 255], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 255, 255], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [255, 255, 255], [0, 255, 0], [0, 0, 0], [0, 255, 0], [255, 255, 255], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [255, 255, 255], [0, 255, 0], [0, 255, 0], [0, 255, 0], [255, 255, 255], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0]],
[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 255, 0], [0, 255, 0], [255, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 255, 0], [255, 0, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [0, 255, 0], [255, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0], [0, 0, 0], [0, 255, 0]]]

def show_frame():
    for x in FRAMES:
        sh.set_pixels(x)
        time.sleep(1)

def main():
    try:
        while True:
            show_frame()
    except (KeyboardInterrupt, SystemExit):
        sys.exit()
            
if __name__ == '__main__':
    main()