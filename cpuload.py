#!/usr/bin/env python

from __future__ import division, print_function
from sense_hat import SenseHat
import argparse, sys, psutil

#parser = argparse.ArgumentParser()
#args = parser.parse_args()

sense = SenseHat()
#sense.clear()
#print(sense.rotation)
#sense.set_rotation(270, False)
#sense.flip_v()

MAX_CPU_LOAD = 80

green = (55, 255, 0)
red = (255, 0, 0)
orange = (255, 190, 0)

lvl = [green, green, orange, orange, red, red, red, red]
    
def check(cpu=None):
    sense.set_rotation(270, False)
    
    cpu = cpu or psutil.cpu_percent()
    cpu = float(cpu)
    
    cpu = int(min(cpu, MAX_CPU_LOAD) * 7 // MAX_CPU_LOAD)
    
    for i in range(0, cpu + 1):
        #print(i)
        sense.set_pixel(i, 0, lvl[cpu])
        
    for i in range(cpu + 1, 8):
        #print(i)
        sense.set_pixel(i, 0, 0, 0, 0)
        
    sense.set_rotation(0, False)

def main(args):
    try:
        cpu = int(args[1]) if len(args) > 1 else None
        
        if cpu is None:
            pass
        elif cpu > 100 or cpu < 0:
            raise Exception("Not in the range 0 - 100")
        
        check(cpu)
    except (KeyboardInterrupt, SystemExit):
        pass
    
if __name__ == "__main__":
    main(sys.argv)