#!/usr/bin/env python

import csv, sys, logging, argparse
from datetime import datetime
import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as md
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

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
    
    with open('/tmp/senselog.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        reader.next() # skip the first line
        
        _logger.debug('Plot data: ' + plotdata)
        
        for row in reader:
            _logger.debug(row)
            #x.append(datetime.strptime( row[16], "%Y-%m-%d %H:%M:%S.%f"))
            x.append(datetime.strptime( row[16], "%Y-%m-%dT%H:%M:%S.%f"))
            y.append(row[CSV_MAP.get(plotdata, 0)])
        
        plt.plot(x, y)
        plt.gca().xaxis.set_major_formatter(md.DateFormatter("%Y-%m-%d %H:%M"))
        plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)

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
