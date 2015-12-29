#!/usr/bin/env python

from sense_hat import SenseHat
import time

sense = SenseHat()
sense.set_imu_config(True, True, True)  # gyroscope only

def main():
    try:
        while True:
            #pitch, roll, yaw = sense.get_orientation().values()
            orientation = sense.get_orientation()
            #print("pitch=%s, roll=%s, yaw=%s" % (pitch, roll, yaw))
            print("pitch={pitch:.5f}, roll={roll:.5f}, yaw={yaw:.5f}".format(**orientation))

            time.sleep(0.01)
    except (KeyboardInterrupt, SystemExit):
        pass
    
if __name__ == '__main__':
    main()