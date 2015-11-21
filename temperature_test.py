#! /usr/bin/env python

from sense_hat import SenseHat
sense = SenseHat()

temp = sense.get_temperature_from_humidity()
print("Temperature from humidity sensor: %s C" % temp)

temp = sense.get_temperature_from_pressure()
print("Temperature from pressure sensor: %s C" % temp)