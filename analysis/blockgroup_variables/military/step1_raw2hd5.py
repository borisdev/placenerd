"""NHGIS attribute values convert to a pyTable 
"""
import csv
import pysal
from tables import *
import sys
sys.path.append("../../../../tools/parsers")
from nhgis2pytable import convert

## SORT by shp index 

#TypeError: invalid type (<type 'str'>) for column ``total_mobility_pop``

if __name__ == '__main__':
    #map new fields to fields in NHGIS csv

    var_mapping={
        "total_military":  "QXIE001"
        }

    raw="/Users/slow/workspace/geoscore/S3/attributes/usa_blockgroups/military/military.csv"
    convert(var_mapping,raw,"military")
