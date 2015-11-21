#!/usr/bin/env python3

import time, pylog
from sense_hat import SenseHat

sense = SenseHat()

while True:
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()

    t = round(t, 5)
    p = round(p, 5)
    h = round(h, 5)

    msg = "Temperature = %s, Pressure=%s, Humidity=%s" % (t,p,h)
    #print(msg)
    pylog.log(msg)
    #sense.show_message(msg, scroll_speed=0.05, text_colour=[0,100,0])
    time.sleep(300)
