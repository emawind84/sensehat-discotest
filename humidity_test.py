#!/usr/bin/env python3

import time, pylog, maker_request
from sense_hat import SenseHat

sense = SenseHat()
prev_h = sense.get_humidity()

def detected(d):
    pylog.log('Humidity changed of %s' % d[0])
    data = {'value1': round(d[0], 5)}
    maker_request.send('humidity_changed', data)
    time.sleep(5)
    
count = 0
while True:
    count += 1
    h = sense.get_humidity()
    diff = abs(h - prev_h)    
    # update every tot seconds
    if count % 5 == 0:
        #print('#updating')
        prev_h = h
        
    if diff > 1.5:
        detected([diff])
    #print(diff)
    pylog.log(diff)
    #sense.show_message(msg, scroll_speed=0.05, text_colour=[0,100,0])
    time.sleep(0.05)
