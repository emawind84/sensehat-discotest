#!/usr/bin/env python
"""Tiny UI for Sense Hat where you can attach 
and view on the matrix screen any data you want. 
Just add your program as a SenseRunnable and there you go!"""

from __future__ import division, print_function

import sys
import time
import os
from sense_hat import SenseHat, SenseStick
from threading import Thread, Event
import cpuload
import diskio
import christmas
import christmas2
import logging
import ciao
import merrychristmas

__author__ = "Emanuele Disco"
__copyright__ = "Copyright 2017"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "emanuele.disco@gmail.com"
__status__ = "Production"

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)
#logger = logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# define the number of screens the ui will manage
screen = [1, 2, 3, 4, 5, 6, 7, 8]

sense = SenseHat()
sense.clear()
#sense.low_light = True
stick = SenseStick()
LED_COLOR = (255, 0, 0)

proc_stop = Event()
proc_stop.set()
proc_running = False
proc_pause = Event()

procs = {}

class SenseRunnable(object):
    """This class is a wrapper for the process that will be executed on the display"""
    
    def __init__(self, _run, with_shift=False):
        self._run = _run
        self.with_shift = with_shift
    
    def run(self):
        self._run()
        if self.with_shift:
            move()

def init_processes():
    global procs
    # define here processes to run on the screens
    procs = { 
        1: SenseRunnable(cpuload.check, with_shift=True),
        2: SenseRunnable(diskio.checkRead, with_shift=True),
        3: SenseRunnable(diskio.checkWrite, with_shift=True),
        4: SenseRunnable(christmas2.show_frame),
        5: SenseRunnable(christmas.show_frame),
        6: SenseRunnable(ciao.show_frame),
        7: SenseRunnable(merrychristmas.show_message)
    }
    
def no_process():
    logger.info('No process set for the screen %s' % screen[0])
    sense.rotation = 0
    sense.set_pixel(screen[0] - 1, 0, (255, 0, 0))
    
    time.sleep(1)

def quit():
    logger.info('Bye bye!')
    
    # stop thread in background
    stop_process()
    
    sense.clear()
    sys.exit()

def activateScreen(idx):
    global screen
    logger.info('Activating screen %s...' % screen[0] )
    
    # stop thread in background
    stop_process()
    
    if idx == screen[0]:
        pass
    elif idx > screen[0]:
        # go right
        screen = screen[1:] + screen[:1]
    else:
        # go left
        screen = screen[-1:] + screen[:-1]
        
    showActiveScreen()
    

def showActiveScreen():
    logger.info('Screen active: %s' % screen[0])
    
    pause_process()
    
    sense.show_letter(str(screen[0]), text_colour=LED_COLOR)
    time.sleep(1)
    sense.clear()
    
    unpause_process()

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

def run_process(stop_event):
    logger.info('Starting process on screen %s...' % screen[0] )
    global proc_running
    proc_running = True
    
    while True and not stop_event.is_set():
        if not proc_pause.is_set():
            # run process here default to no_process
            procs.get(screen[0], SenseRunnable(no_process)).run()
                        
        time.sleep(0.2)
        
    proc_running = False
        
def stop_process():
    logger.info('Stopping process on screen %s...' % screen[0] )
    # stop thread in background
    proc_stop.set()
    
    # wait until the process stop
    while proc_running:
        time.sleep(0.1)
    
    # clear led screen after process end
    sense.clear()
    
def pause_process():
    logger.info('Pausing process on screen %s...' % screen[0] )
    proc_pause.set()
    
def unpause_process():
    logger.info('Unpausing process on screen %s...' % screen[0] )
    proc_pause.clear()
        
def main():    
    try:
        init_processes()
        
        activateScreen(1)
        
        for event in eventIterator():
            time.sleep(0.2)
            
            if event and event.state == 1:
                key = int(event.key)
                if key == stick.KEY_LEFT:
                    activateScreen(screen[0] - 1)
                    
                if key == stick.KEY_RIGHT:
                    activateScreen(screen[0] + 1)
                    
                if key == stick.KEY_ENTER:
                    showActiveScreen()

            if proc_stop.is_set():
                proc_stop.clear()
                Thread(target=run_process, args=(proc_stop,)).start()
        
    except (KeyboardInterrupt, SystemExit):
        quit()
            
if __name__ == '__main__':
    main()
