#!/usr/bin/env python

"""rawRssiScanner.py: Scans the WiFi environment for RSSI values from WiFi beacon packets."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

from wifiFingerprint import wifiFingerprint
from datetime import datetime
import time
import json
import sys
import urllib
import urllib2
import raw_data_pb2

# This is an example of scanning the environment for RSSI values and storing them as a message in the raw data database

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'test_db'

# The ID of the collection in the database
coll_id = 'test_coll'

NUMBER_OF_SCANS = 1

if __name__ == '__main__':
    
    raw_data_collection = raw_data_pb2.RawRFReadingCollection() 
    raw_data_collection.metadata_id = "1"
    raw_data_collection.data_id = "1"
    raw_data_collection.meas_number = NUMBER_OF_SCANS

    for scans in range(1, NUMBER_OF_SCANS + 1):
        fpf = wifiFingerprint()
        fpf.scan(1)
        fp = fpf.getFingerprint()
        for key in fp.keys():
            raw_data_reading = raw_data_collection.raw_measurement.add()
            x = datetime.utcnow()
            raw_data_reading.timestamp_utc = timestamp_utc = int(time.mktime(x.timetuple()))
            raw_data_reading.receiver_id = 'MacBook'
            raw_data_reading.receiver_location.coordinate_x = 1
            raw_data_reading.receiver_location.coordinate_y = 1
            raw_data_reading.receiver_location.coordinate_z = 1
            raw_data_reading.receiver_location.room_label = 'test'
            raw_data_reading.run_nr = scans
            raw_data_reading.sender_bssid = key
            raw_data_reading.sender_id = fp[key]['ssid']
            raw_data_reading.rssi = int(fp[key]['rssi'][0])
            raw_data_reading.channel = fp[key]['channel']

    obj = raw_data_collection.SerializeToString()

    req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id, headers={"Content-Type": "application/x-protobuf"}, data = obj)
    resp = urllib2.urlopen(req)
    print json.loads(resp.read())