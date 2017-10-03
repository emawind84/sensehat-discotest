#!/usr/bin/env python

import sys
import logging
import json
import requests
import dateutil.parser
import pygal
from pygal import Config

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

x = []
y = []
plotdata = 'temp_h'

PLOT_SAVE_PATH = '/home/pi/sensehat-datalog/plot'

CSV_MAP = {'temp_h': 0, 'temp_p': 1, 
           'humidity': 2, 'pressure': 3, 
           'pitch': 4, 'roll': 5, 'yaw': 6, 
           'mag_x': 7, 'mag_y': 8, 'mag_z': 9,
           'acc_x': 10, 'acc_y': 11, 'acc_z': 12,
           'gyro_x': 13, 'gyro_y': 14, 'gyro_z': 15,
           'timestamp': 16}

config = Config()
config.show_legend = False
config.human_readable = True

def main():
    
    s = requests.session()
    query = {
        "query": {
            "range": {
                "timestamp": {
                    "gte": "now-4d/d",
                    "lte": "now/d"
                }
            }
        },
        "size": 2000,
        "sort": [{
            "timestamp": { "order": "asc" }
        }]
    }
    result = s.get('http://localhost:9200/sense/stats/_search', data=json.dumps(query))
    jresult = result.json()
    datalist = jresult['hits']['hits']

    _t = len(datalist) // 40
    _i = -1
    for rowdata in datalist:
        _i += 1
        if _i % _t != 0:
            continue
            
        rowdata = rowdata['_source']
        _logger.debug(rowdata)

        x.append(dateutil.parser.parse(rowdata['timestamp']))
        y.append(rowdata[plotdata])
        
    hist = pygal.Line(x_label_rotation=20, 
                      height=340, 
                      x_labels_major_count=10, 
                      show_minor_x_labels=False
                      )
    hist.x_labels = map(lambda d: d.strftime('%Y-%m-%d %H:%M'), x)
    hist.x_title = "timestamp"
    hist.y_title = plotdata
    hist.add('', y)

    hist.render_to_file(PLOT_SAVE_PATH + '/senselog.svg')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in CSV_MAP:
        plotdata = sys.argv[1]
    
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', '-d', action='store_true', dest='debug', help='More logging on console')
    _args = parser.parse_args()
    
    if _args.debug:
        _logger.setLevel(logging.DEBUG)
    '''
    
    main()
