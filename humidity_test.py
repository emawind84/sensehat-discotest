#!/usr/bin/env python3

import time, maker_request, argparse, logging
from sense_hat import SenseHat
from pylog import PyLog

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

_args = {}
sense = SenseHat()
pylog = PyLog('log/humidity.log')
pylog.WRITE_FREQ = 1

def detected(d):
    pylog.log('Humidity changed of %s' % d[0])
    
    if _args.maker:
        data = {'value1': round(d[0], 5)}
        maker_request.send('humidity_changed', data)
    
    time.sleep(5)
    
def main():
    try:
        prev_h = sense.get_humidity()
        count = 0
        while True:
            time.sleep(0.1)
            count += 1
            
            h = sense.get_humidity()
            _logger.debug(h)
            
            if h != 0 and prev_h != 0:
                diff = abs(h - prev_h)
                
                if diff > 1.5:
                    detected([diff])
                
            # update every tot seconds
            if count % 10 == 0:
                prev_h = h
                count = 0

            #pylog.log(diff)
            #sense.show_message(msg, scroll_speed=0.05, text_colour=[0,100,0])
            
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':   
    parser = argparse.ArgumentParser()
    parser.add_argument('--maker', action='store_true', dest='maker', help='Send notification through Maker Channel')
    parser.add_argument('--debug', action='store_true', dest='debug', help='More logging on console')
    _args = parser.parse_args()
    
    if _args.debug:
        _logger.setLevel(logging.DEBUG)

    main()