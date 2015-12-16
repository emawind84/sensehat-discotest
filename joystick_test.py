from __future__ import print_function

import pygame, sys, time, os, atexit
from pygame.locals import *
from sense_hat import SenseHat

#os.environ["SDL_VIDEODRIVER"] = "dummy"

hmov = [0, 1, 2, 3, 4, 5, 6, 7]
vmov = [0, 1, 2, 3, 4, 5, 6, 7]
LED_COLOR = (255, 0, 0)

pygame.init()
#pygame.display.set_mode()
#pygame.display.init()
pygame.display.set_mode((640, 480))
#screen = pygame.display.set_mode((1,1))

sense = SenseHat()
sense.clear()

def goodbye(name):
    print('Goodbye, %s' % name)

def eventIterator():
    while True:
        yield pygame.event.wait()
        while True:
            event = pygame.event.poll()
            if event.type == NOEVENT:
                break
            else:
                yield event

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
    print('Exiting...')
    time.sleep(1)
    sense.clear()
    pygame.quit()
    sys.exit()

sense.set_pixel(0, 0, 255, 0 , 0)
atexit.register(goodbye, name='Emanuele')

for event in eventIterator():
    print(event)
    if event.type == QUIT:
        quit()
    elif event.type == KEYDOWN:
        if event.key == K_RETURN:
            print('ENTER')
            pygame.event.post(pygame.event.Event(QUIT))
        if event.key == K_LEFT:
            print('LEFT')
            moveLeft()
        if event.key == K_RIGHT:
            print('RIGHT')
            moveRight()
        if event.key == K_UP:
            print('UP')
            moveUp()
        if event.key == K_DOWN:
            print('DOWN')
            moveDown()
    