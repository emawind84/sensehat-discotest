#!/usr/bin/env python
"""Detect acceleration anomalies using Sense Hat, 
logging and sending notification via Twitter and Maker.
Data are saved on Elasticsearch engine."""

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
from ttytter import Ttytter

__author__ = "Emanuele Disco"
__copyright__ = "Copyright 2017"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "emanuele.disco@gmail.com"
__status__ = "Production"

sense = SenseHat()
sense.clear()

min_difference = 0.01
anomalies_detected = False
anomalies = 0
current_data = []
stop_event = Event()
pylog = PyLog(filename='log/mov_detector.log', write_freq=10)

# Lets make some logs!
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

def log_to_file(d):
    _logger.debug('Logging anomalies...')
    pylog.log('Detected movement x: %s, y: %s, z: %s' % (d['x'], d['y'], d['z']))
    
def show_led(stop_event):
    while True and not stop_event.is_set():
        time.sleep(0.1)
        if not anomalies_detected:
            continue
        sense.set_pixel(0, 0, 255, 0, 0)
        time.sleep(0.1)
        sense.set_pixel(0, 0, 0, 0, 0)
        _logger.debug('Led On')

def send_maker_notification(stop_event):
    while True and not stop_event.is_set():
        time.sleep(0.1)
        if not anomalies_detected:
            continue

        if anomalies > 20:
            data = {'value1': round(current_data['x'], 5), 
                    'value2': round(current_data['y'], 5),
                    'value3': round(current_data['z'], 5)
                    }
            maker_request.send('mov_detected', data)
            time.sleep(30)
        
def send_twitter_msg(stop_event):
    while True and not stop_event.is_set():
        time.sleep(0.1)
        if not anomalies_detected:
            continue
            
        if anomalies > 10:
            Ttytter().send('Detected %s acceleration anomalies %06.5fg, %06.5fg, %06.5fg.' 
                           % (anomalies, 
                              current_data['x'], 
                              current_data['y'], 
                              current_data['z']
                             )
                          )
            time.sleep(30)
        
def log_to_es(d):
    d['timestamp'] = str(datetime.utcnow().isoformat())
    es_data_import.post('sense_acc', 'data', d)

def do_before_exit():
    _logger.info('Exiting...')
    stop_event.set()
    sense.clear()

def find_mean():
    xx = []
    yy = []
    zz = []
    for d in range(50):
        x, y, z = sense.get_accelerometer_raw().values()
        if abs(x) > 1.2: continue
        if abs(y) > 1.2: continue
        if abs(z) > 1.2: continue
        xx.append(x)
        yy.append(y)
        zz.append(z)
        time.sleep(0.01)
    
    x = sum(xx) / float(len(xx))
    y = sum(yy) / float(len(yy))
    z = sum(zz) / float(len(zz))

    return { 'x': round(x, 5), 'y': round(y, 5), 'z': round(z, 5)}
    
def run():
    global anomalies_detected
    global anomalies
    global current_data
    
    mean_acc = sense.get_accelerometer_raw()
    anomalies = 0
    
    while True:
        clean_data = True
        current_data = acc = sense.get_accelerometer_raw()
        d = (abs(mean_acc['x'] - acc['x']), 
             abs(mean_acc['y'] - acc['y']), 
             abs(mean_acc['z'] - acc['z']))
        _logger.debug('%06.5f, %06.5f, %06.5f' % d)
        t = anomalies
        for val in d:
            if val > 1:
                _logger.debug('Rejecting data %s.' % val)
                clean_data = False
                break  # reject data

            if val > min_difference:
                anomalies += 1
                break
        
        if clean_data and t == anomalies:
            anomalies_detected = False
            anomalies = 0

        if clean_data and anomalies >= 2:
            _logger.debug('%s anomalies detected.' % anomalies)
            anomalies_detected = True
            log_to_file(acc)
            log_to_es(acc)
            
        time.sleep(0.01)
    
def main():
    _parser = argparse.ArgumentParser()
    _parser.add_argument('-d', '--debug', action='store_true', dest='debug', help='More logging on console')
    _args = _parser.parse_args()
  
    if _args.debug:
        _logger.setLevel(logging.DEBUG)
        
    try:
        # red led on sense hat matrix
        Thread(target=show_led, args=(stop_event,)).start()
        
        # twitter alert
        #Thread(target=send_twitter_msg, args=(stop_event,)).start()

        # maker alert
        #Thread(target=send_maker_notification, args=(stop_event,)).start()
        
        # main thread
        run()

        # do before normal exit
        do_before_exit()
    except (KeyboardInterrupt, SystemExit):
        do_before_exit()        
        
if __name__=='__main__':
    main()
