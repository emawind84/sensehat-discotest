#!/usr/bin/env python3

from sense_hat import SenseHat
import atexit, time

sense = SenseHat()

def goodbye(name):
    print('Goodbye, %s' % name)
    
def main():
    try:
        while True:
            #x, y, z = sense.get_accelerometer_raw().values()

            acc = sense.get_accelerometer_raw()
            x = acc['x']
            y = acc['y']
            z = acc['z']

            x = round(x, 5)
            y = round(y, 5)
            z = round(z, 5)

            print("x=%s, y=%s, z=%s" % (x, y, z))

            time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        pass

atexit.register(goodbye, name='Emanuele')
        
if __name__=='__main__':
    main()