"""NHGIS attribute values convert to a pyTable 
"""
import csv
import pysal
from tables import *
import sys
sys.path.append("../../../../tools/parsers")
import nhgis2pytable_blkgrp_var_with_geos
## SORT by shp index 

#TypeError: invalid type (<type 'str'>) for column ``total_mobility_pop``

if __name__ == '__main__':
    #map new fields to fields in NHGIS csv

    var_mapping={
        "total":  "QSEE001"
        }

    raw="/Users/slow/workspace/geoscore/S3/attributes/usa_blockgroups/age/age.csv"
    nhgis2pytable_blkgrp_var_with_geos.convert(var_mapping,raw,"nested_geo_with_pop")
