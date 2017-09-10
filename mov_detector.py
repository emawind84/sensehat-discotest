#!/usr/bin/env python

from __future__ import print_function

import sys
import time
import atexit
import logging
import argparse
from threading import Thread, Event
from sense_hat import SenseHat
import maker_request
import es_data_import
from pylog import PyLog
from datetime import datetime

sense = SenseHat()
sense.clear()

min_difference = 0.005
anomalies_detected = False
stop_event = Event()
pylog = PyLog(filename='log/mov_detector.log', write_freq=10)

# Lets make some logs!
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

def log_anomaly(d):
    _logger.debug('Logging anomalies...')
    pylog.log('Detected movement x: %s, y: %s, z: %s' % d)
    '''
    data = {'value1': round(d[0], 3), 
            'value2': round(d[1], 3),
            'value3': round(d[2], 3)}
    maker_request.send('mov_detected', data)
    '''
    #time.sleep(5)
    
def show_led(stop_event):
    global anomalies_detected
    
    while True and not stop_event.is_set():
        time.sleep(0.1)
        if not anomalies_detected:
            continue
        sense.set_pixel(0, 0, 255, 0, 0)
        time.sleep(0.1)
        sense.set_pixel(0, 0, 0, 0, 0)
        _logger.debug('Led On')
        
def create_es_index(d):
    d['timestamp'] = str(datetime.utcnow().isoformat())
    es_data_import.post('sense_acc', 'data', d)

def do_before_exit():
    _logger.info('Exiting...')
    stop_event.set()
    sense.clear()
    
def run():
    global anomalies_detected
    
    mean_acc = sense.get_accelerometer_raw()
    anomalies = 0
    
    while True:  
        acc = sense.get_accelerometer_raw()
        d = (abs(mean_acc['x'] - acc['x']), 
             abs(mean_acc['y'] - acc['y']), 
             abs(mean_acc['z'] - acc['z']))
        t = anomalies
        for val in d:
            if val > min_difference:
                anomalies += 1
                break
        _logger.debug('%06.5f, %06.5f, %06.5f' % d)
        if t == anomalies:
            anomalies_detected = False
            anomalies = 0
            mean_acc = acc

        if anomalies >= 2:
            _logger.debug('Anomalies detected')
            anomalies_detected = True
            log_anomaly(d)
            create_es_index(acc)
            
        time.sleep(0.1)
    
def main():
    _parser = argparse.ArgumentParser()
    _parser.add_argument('-d', '--debug', action='store_true', dest='debug', help='More logging on console')
    _args = _parser.parse_args()
  
    if _args.debug:
        _logger.setLevel(logging.DEBUG)
        
    try:
        # sub thread
        Thread(target=show_led, args=(stop_event,)).start()
        
        # main thread
        run()
    except (KeyboardInterrupt, SystemExit):
        do_before_exit()
        
        
if __name__=='__main__':
    main()
