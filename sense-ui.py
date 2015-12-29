#!/usr/bin/env python
from __future__ import division, print_function

import sys, time, os, atexit, cpuload, diskio
from sense_hat import SenseHat, SenseStick

screen = [1, 2, 3, 4]
screen_idx = 1

sense = SenseHat()
sense.clear()
#sense.low_light = True
stick = SenseStick()
LED_COLOR = (255, 0, 0)
    
def quit():
    time.sleep(1)
    sense.clear()
    sys.exit()

def activateScreen(idx):
    global screen
    
    if idx == screen[0]:
        pass
    elif idx > screen[0]:
        # go right
        screen = screen[1:] + screen[:1]
    else:
        # go left
        screen = screen[-1:] + screen[:-1]
        
    showActivateScreen()
    

def showActivateScreen():
    print('Screen active: %s' % screen[0])
    sense.show_letter(str(screen[0]), text_colour=LED_COLOR)
    time.sleep(1)
    sense.clear()

def eventIterator():
    while True:
        ret = stick.wait(0)
        if ret == True:
            yield stick.read()
        else:
            yield False

def move():
    sense.set_rotation(0, False)

    for x in range(1, 8):
        for y in range(0, 8):
            picolor = sense.get_pixel(x, y)
            sense.set_pixel(x - 1, y, picolor);
    sense.set_rotation(0, False)
    
def main():
    try:
        activateScreen(1)
        
        for event in eventIterator():
            time.sleep(0.2)
            move()
            if event and event.state == 1:
                key = int(event.key)
                if key == stick.KEY_LEFT:
                    activateScreen(screen[0] - 1)
                    
                if key == stick.KEY_RIGHT:
                    activateScreen(screen[0] + 1)
                    
                if key == stick.KEY_ENTER:
                    showActivateScreen()

            if screen[0] == 1:
                cpuload.check()

            if screen[0] == 2:
                diskio.check('read')

            if screen[0] == 3:
                diskio.check('write')
            
            if screen[0] == 4:
                pass
        
    except (KeyboardInterrupt, SystemExit):
        quit()
            
if __name__ == '__main__':
    main()