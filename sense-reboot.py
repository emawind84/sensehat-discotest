#!/usr/bin/env python
from __future__ import print_function

import sys, time, subprocess
from sense_hat import SenseStick

press_delay = 50
stick = SenseStick()

def eventIterator():
    while True:
        yield stick.read()
        
def reboot():
    time.sleep(1)
    print("Rebooting system...")
    subprocess.call(['shutdown', '-r', '0'])
    sys.exit()
    
def quit():
    time.sleep(1)
    sys.exit()

def loop():
    _p = press_delay
    for event in eventIterator():
        time.sleep(0.01)
        #print(event)
        if event.state == 2:
            if event.key == 28:
                _p -= 1
                if _p < 0:
                    reboot()
        else:
            _p = press_delay
def main():
    try:
        loop();
    except (KeyboardInterrupt, SystemExit):
        quit()
            
if __name__ == '__main__':
    main()