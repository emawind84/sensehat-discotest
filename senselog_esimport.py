#!/usr/bin/env python3

import json, csv, requests, logging, argparse
import dateutil.parser

CSV_MAP = ['temp_h','temp_p','humidity','pressure',
           'pitch','roll','yaw',
           'mag_x','mag_y','mag_z',
           'acc_x','acc_y','acc_z',
           'gyro_x','gyro_y','gyro_z',
           'timestamp']

# ElasticSearch parameters
ES_HOST = '127.0.0.1'
ES_PORT = '9200'
ES_INDEX = 'sense'
ES_TYPE = 'stats'

CSV_FILE_PATH = 'log/senselog.csv'

# Lets make some logs!
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s')
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

def main():
    s = requests.Session()
    
    #r = s.delete( "http://%s:%s/%s/" % (ES_HOST, ES_PORT, ES_INDEX) )
    #_logger.debug(r.text)
    
    with open(CSV_FILE_PATH, 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        
        # skip the first line is has header
        next(reader)
        
        for row in reader:
            data =  dict(zip(CSV_MAP, row))
            
            # added time zone because data on the csv file have offset
            timestamp = dateutil.parser.parse( data['timestamp'] + '+0900' )
            # format the date with the offset in order to index the correct date
            data['timestamp'] = timestamp.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')
            
            # let's prevent es from overwriting (creating new version) the same data if already exists
            # add the querystring: "op_type=create" to prevent from creating new version
            # https://www.elastic.co/guide/en/elasticsearch/guide/current/create-doc.html#create-doc
            r = s.put( "http://%s:%s/%s/%s/%s?op_type=create" % 
                      (ES_HOST, ES_PORT, ES_INDEX, ES_TYPE, data['timestamp']), 
                      data=json.dumps(data))
            _logger.debug(r.text)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log', action='store', dest='logfile', help='The log file to import into elasticsearch engine')
    args = parser.parse_args()

    if args.logfile:
        CSV_FILE_PATH = args.logfile
        
    main()
