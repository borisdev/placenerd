"""NHGIS attribute values convert to a pyTable 
"""
import csv
import pysal
from tables import *
import sys
sys.path.append("../../../../tools/parsers")
from nhgis2pytable import convert

## SORT by shp index 

"""
QYIE001:     Total
QYIE002:     For rent
QYIE003:     Rented, not occupied
QYIE004:     For sale only
QYIE005:     Sold, not occupied
QYIE006:     For seasonal, recreational, or occasional use
QYIE007:     For migrant workers
QYIE008:     Other vacant

"""
#TypeError: invalid type (<type 'str'>) for column ``total_mobility_pop``

if __name__ == '__main__':
    #map new fields to fields in NHGIS csv

    var_mapping={
        "total":  "QYIE001"
        ,"forsale": "QYIE004" 
        ,"vacant": "QYIE008" 
        }

    raw="/Users/slow/workspace/geoscore/S3/attributes/usa_blockgroups/forsale_vacant/forsale_vacant.csv"
    convert(var_mapping,raw,"forsale_vacant")
