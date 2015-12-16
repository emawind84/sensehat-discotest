#!/usr/bin/env python
from __future__ import print_function

import sys, time, os, atexit
from sense_hat import SenseHat, SenseStick

hmov = [0, 1, 2, 3, 4, 5, 6, 7]
vmov = [0, 1, 2, 3, 4, 5, 6, 7]
LED_COLOR = (255, 0, 0)

sense = SenseHat()
sense.clear()
sense.set_pixel(0, 0, 255, 0 , 0)

stick = SenseStick()

def goodbye(name='Emanuele'):
    print('Goodbye, %s!' % name)

def eventIterator():
    while True:
        yield stick.read()

def moveLeft():
    global hmov
    sense.set_pixel(hmov[0], vmov[0], 0, 0, 0)
    hmov = hmov[-1:] + hmov[:-1]
    sense.set_pixel(hmov[0], vmov[0], LED_COLOR)

def moveRight():
    global hmov
    sense.set_pixel(hmov[0], vmov[0], 0, 0, 0)
    hmov = hmov[1:] + hmov[:1]
    sense.set_pixel(hmov[0], vmov[0], LED_COLOR)

def moveDown():
    global vmov
    sense.set_pixel(hmov[0], vmov[0], 0, 0, 0)
    vmov = vmov[1:] + vmov[:1]
    sense.set_pixel(hmov[0], vmov[0], LED_COLOR)
    
def moveUp():
    global vmov
    sense.set_pixel(hmov[0], vmov[0], 0, 0, 0)
    vmov = vmov[-1:] + vmov[:-1]
    sense.set_pixel(hmov[0], vmov[0], LED_COLOR)
    
def quit():
    time.sleep(1)
    sense.clear()
    sys.exit()

atexit.register(goodbye)
    
def loop():
    for event in eventIterator():
        print(event)
        if event.state == 1:
            if event.key == 28:
                print('ENTER')
                quit()
            if event.key == 105:
                print('LEFT')
                moveLeft()
            if event.key == 106:
                print('RIGHT')
                moveRight()
            if event.key == 103:
                print('UP')
                moveUp()
            if event.key == 108:
                print('DOWN')
                moveDown()
            
def main():
    try:
        loop();
    except (KeyboardInterrupt, SystemExit):
        quit()
            
if __name__ == '__main__':
    main()