#!/usr/bin/env python

from sense_hat import SenseHat
from datetime import datetime
from threading import Thread, Event
from pylog import PyLog
import time, sys, argparse, json, logging, atexit

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('-j', '--json', action='store_true', dest='jsonout', help='print data directly on console')
parser.add_argument('-l', '--log', action='store', dest='logfile', help='use this log file for logging data')
args = parser.parse_args()

DELAY = 300

sense = SenseHat()
sense_data = []
header = ['temp_h', 'temp_p', 'humidity', 'pressure',
          'pitch', 'roll', 'yaw',
          'mag_x', 'mag_y', 'mag_z',
          'acc_x', 'acc_y', 'acc_z',
          'gyro_x', 'gyro_y', 'gyro_z',
          'timestamp']

pylog = PyLog()
pylog.FILE_NAME = 'senselog.csv'
#pylog.WRITE_FREQ = 1

timed_log_stop = Event()

def quit():
    timed_log_stop.set()
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
    
    sense_data.append(str(datetime.now()))
    
    return sense_data


def timed_log(stop_event):
    global sense_data
    
    while not stop_event.is_set():
        pylog.log_data(sense_data)
        
        # wait for the delay but check every 0.2s if the thread has been stopped
        for i in range(int(DELAY//0.2)):
            time.sleep(0.2)
            if stop_event.is_set():
                break

def main():
    global sense_data
    
    try:
        pylog.set_header(header)
        
        if DELAY > 0:
            sense_data = get_sense_data()
            t = Thread(target=timed_log, args=(timed_log_stop,))
            t.start()
        
        while True:
            time.sleep(0.1)
            sense_data = get_sense_data()
            #print(sense_data)
            
            if DELAY == 0:
                pylog.log_data(sense_data)
            
    except (KeyboardInterrupt, SystemExit):
        quit()

if __name__ == '__main__':
    if args.logfile:
        pylog.FILE_NAME = args.logfile
        
    if args.jsonout:
        data = get_sense_data()
        data = {k: v for (k,v) in zip(header, data)}
        #print(data)
        print(json.dumps(data))
    else:
        main()