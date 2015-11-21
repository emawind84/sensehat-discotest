#!/usr/bin/env python3

from sense_hat import SenseHat
import atexit, time

sense = SenseHat()

def goodbye(name):
    print('Goodbye, %s' % name)
    
def main():
    while True:
        #x, y, z = sense.get_accelerometer_raw().values()

        acc = sense.get_accelerometer_raw()
        x = acc['x']
        y = acc['y']
        z = acc['z']

        x = round(x, 2)
        y = round(y, 2)
        z = round(z, 2)

        print("x=%s, y=%s, z=%s" % (x, y, z))
        
        time.sleep(0.5)

atexit.register(goodbye, name='Emanuele')
        
if __name__=='__main__':
    main()