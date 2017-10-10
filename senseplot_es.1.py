#!/usr/bin/env python

import csv
import sys
import logging
import argparse
import matplotlib
import requests
import json
import dateutil.parser

matplotlib.use("Agg")

import matplotlib.dates as md
import matplotlib.pyplot as plt

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
        
    plt.plot(x, y)
    plt.gca().xaxis.set_major_formatter(md.DateFormatter("%Y-%m-%d %H:%M"))
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)

    plt.axhline(0, color='black', lw=2)
    plt.xlabel("timestamp")
    plt.ylabel(plotdata)
    plt.gcf().autofmt_xdate()
    #plt.savefig(PLOT_SAVE_PATH + "/senselog.png")
    plt.savefig(PLOT_SAVE_PATH + "/senselog.png", bbox_inches = "tight")

    plt.clf()

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
