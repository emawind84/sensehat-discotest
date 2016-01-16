#!/usr/bin/env python
from __future__ import division, print_function

import sys, time, os, atexit, cpuload, diskio, christmas, christmas2
from sense_hat import SenseHat, SenseStick
from threading import Thread, Event

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

def init_processes():
    global procs
    # define here processes to run on the screens
    procs = { 
        1: (move, cpuload.check),
        2: (move, diskio.checkRead),
        3: (move, diskio.checkWrite),
        4: (christmas2.show_frame,),
        5: (christmas.show_frame,)
    }
    
def no_process():
    print('No process set for the screen %s' % screen[0])
    sense.rotation = 0
    sense.set_pixel(screen[0] - 1, 0, (255, 0, 0))

def quit():
    print('Bye bye!')
    time.sleep(1)
    
    # stop thread in background
    stop_process()
    
    sense.clear()
    sys.exit()

def activateScreen(idx):
    global screen
    print('Activating screen %s...' % screen[0] )
    
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
    print('Screen active: %s' % screen[0])
    
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

def run_process(arg1, stop_event):
    print('Starting process on screen %s...' % screen[0] )
    global proc_running
    proc_running = True
    
    while True and not stop_event.is_set():
        if not proc_pause.is_set():
            # run process here
            for p in procs.get(screen[0], (no_process,)):
                p()
            
        time.sleep(0.2)
        
    proc_running = False
        
def stop_process():
    print('Stopping process on screen %s...' % screen[0] )
    # stop thread in background
    proc_stop.set()
    
    # wait until the process stop
    while proc_running:
        time.sleep(0.1)
    
    # clear led screen after process end
    sense.clear()
    
def pause_process():
    print('Pausing process on screen %s...' % screen[0] )
    proc_pause.set()
    
def unpause_process():
    print('Unpausing process on screen %s...' % screen[0] )
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
                Thread(target=run_process, args=(1, proc_stop)).start()
        
    except (KeyboardInterrupt, SystemExit):
        quit()
            
if __name__ == '__main__':
    main()