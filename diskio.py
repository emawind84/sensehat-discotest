#!/usr/bin/env python
from __future__ import division, print_function
from sense_hat import SenseHat
import psutil, time

sense = SenseHat()
#sense.clear()
#print(sense.rotation)
#sense.set_rotation(270, False)
#sense.flip_v()

green = (55, 255, 0)
red = (255, 0, 0)
orange = (255, 190, 0)

MAX_WRITE_BYTES = 200000
MAX_READ_BYTES = 150000

lvl = [green, green, orange, orange, red, red, red, red]

def poll(interval):
    """Calculate IO usage by comparing IO statics before and
    after the interval.
    Return a tuple including all currently running processes
    sorted by IO activity and total disks I/O activity.
    """
    # first get a list of all processes and disk io counters
    procs = [p for p in psutil.process_iter()]
    for p in procs[:]:
        try:
            p._before = p.io_counters()
        except psutil.Error:
            procs.remove(p)
            continue
    disks_before = psutil.disk_io_counters()

    # sleep some time
    time.sleep(interval)

    # then retrieve the same info again
    for p in procs[:]:
        try:
            p._after = p.io_counters()
            p._cmdline = ' '.join(p.cmdline())
            if not p._cmdline:
                p._cmdline = p.name()
            p._username = p.username()
        except psutil.Error:
            procs.remove(p)
    disks_after = psutil.disk_io_counters()

    # finally calculate results by comparing data before and
    # after the interval
    for p in procs:
        p._read_per_sec = p._after.read_bytes - p._before.read_bytes
        p._write_per_sec = p._after.write_bytes - p._before.write_bytes
        p._total = p._read_per_sec + p._write_per_sec

    disks_read_per_sec = disks_after.read_bytes - disks_before.read_bytes
    disks_write_per_sec = disks_after.write_bytes - disks_before.write_bytes

    # sort processes by total disk IO so that the more intensive
    # ones get listed first
    processes = sorted(procs, key=lambda p: p._total, reverse=True)

    return (processes, disks_read_per_sec, disks_write_per_sec)

def check(type='read'):
    sense.set_rotation(270, False)
    
    ret = poll(1)
    idx = 1 if type == 'read' else 2
    read = int(min(ret[idx], MAX_READ_BYTES) * 7 // MAX_READ_BYTES)
    
    # reading leds
    for i in range(read + 1, 8):
        #print(i)
        sense.set_pixel(i, 7, 0, 0, 0)
        
    for i in range(0, read + 1):
        #print(i)
        sense.set_pixel(i, 7, lvl[read])
    
    sense.set_rotation(0, False)
    
def checkWrite():
    check('write')
    
def checkRead():
    check('read')

def main():
    try:
        interval = 0
        while True:
            ret = poll(interval)
            interval = 1
            
            print(ret[1:])
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    main()