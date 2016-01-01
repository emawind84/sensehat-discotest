#!/usr/bin/env python

from sense_hat import SenseHat
from datetime import datetime
from threading import Thread, Event
import time, pylog, sys

DELAY = 300

sense = SenseHat()
sense_data = []
header = ['temp_h', 'temp_p', 'humidity', 'pressure',
          'pitch', 'roll', 'yaw',
          'mag_x', 'mag_y', 'mag_z',
          'acc_x', 'acc_y', 'acc_z',
          'gyro_x', 'gyro_y', 'gyro_z',
          'timestamp']

pylog.FILE_NAME = 'senselog.csv'
#pylog.WRITE_FREQ = 1

timed_log_stop = Event()

def quit():
    timed_log_stop.set()
    time.sleep(1)
    sys.exit()

def get_sense_data():
    sense_data = []
    
    sense_data.append(sense.get_temperature_from_humidity())
    sense_data.append(sense.get_temperature_from_pressure())
    sense_data.append(sense.get_humidity())
    sense_data.append(sense.get_pressure())
    
    o = sense.get_orientation()
    yaw = o['yaw']
    pitch = o['pitch']
    roll = o['roll']
    
    sense_data.extend([pitch, roll, yaw])
    
    mag = sense.get_compass_raw()
    sense_data.extend([mag['x'], mag['y'], mag['z']])
    
    acc = sense.get_accelerometer_raw()
    sense_data.extend([acc['x'], acc['y'], acc['z']])
    
    gyro = sense.get_gyroscope_raw()
    sense_data.extend([gyro['x'], gyro['y'], gyro['z']])
    
    sense_data.append(datetime.now())
    
    return sense_data


def timed_log(arg1, stop_event):
    global sense_data
    
    while True and not stop_event.is_set():
        pylog.log_data(sense_data)
        time.sleep(DELAY)

def main():
    global sense_data
    
    try:
        pylog.set_header(header)
        
        if DELAY > 0:
            sense_data = get_sense_data()
            Thread(target=timed_log, args=(1, timed_log_stop)).start()
        
        while True:
            time.sleep(0.1)
            sense_data = get_sense_data()
            #print(sense_data)
            
            if DELAY == 0:
                pylog.log_data(sense_data)
            
    except (KeyboardInterrupt, SystemExit):
        quit()

if __name__ == '__main__':
    main()