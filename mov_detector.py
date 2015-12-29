#!/usr/bin/env python

from sense_hat import SenseHat
import time, maker_request, atexit, pylog

sense = SenseHat()
sense.clear()

first = sense.get_accelerometer_raw()
diff = 0.005
active = True

def detected(d):
    print('detected movemement!')
    pylog.log('Detected movement x: %s, y: %s, z: %s' % d)
    data = {'value1': round(d[0], 3), 
            'value2': round(d[1], 3),
            'value3': round(d[2], 3)}
    #maker_request.send('mov_detected', data)
    #time.sleep(5)
    
def show_led():
    while True:
        if not active:
            break
        sense.set_pixel(0, 0, 255, 0, 0)
        time.sleep(1)
        sense.set_pixel(0, 0, 0, 0, 0)
        time.sleep(1)

def goodbye(name):
    sense.clear()
    print('Goodbye, %s' % name)
    
def run():
    global first
    
    dd = 0
    while True:  
        acc = sense.get_accelerometer_raw()
        d = (abs(first['x'] - acc['x']), 
             abs(first['y'] - acc['y']), 
             abs(first['z'] - acc['z']))
        #print(acc)
        t = dd
        for val in d:
            if val > diff:
                dd += 1
                break
        #print('%06.5f, %06.5f, %06.5f' % d)
        if t == dd:
            dd = 0

        if dd >= 2:
            detected(d)
            dd = 0
            first = acc
            
        time.sleep(0.1)
    
def main():
    try:
        run()
    except (KeyboardInterrupt, SystemExit):
        pass
    
atexit.register(goodbye, name='Emanuele')

        
if __name__=='__main__':
    main()
