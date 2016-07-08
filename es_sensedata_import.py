#!/usr/bin/env python

import json, csv, requests, logging
from datetime import datetime

CSV_MAP = ['temp_h','temp_p','humidity','pressure',
           'pitch','roll','yaw',
           'mag_x','mag_y','mag_z',
           'acc_x','acc_y','acc_z',
           'gyro_x','gyro_y','gyro_z',
           'timestamp']

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

def main():
    with open('log/senselog.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        #reader = csv.DictReader(csvfile)
        reader.next() # skip the first line

        for row in reader:
            data =  dict(zip(CSV_MAP, row))
            timestamp = datetime.strptime( data['timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            data['timestamp'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
            r = requests.post("http://203.239.21.69:9200/sense/stats", data=json.dumps(data))
            _logger.debug(r.text)
        
if __name__ == '__main__':
    main()