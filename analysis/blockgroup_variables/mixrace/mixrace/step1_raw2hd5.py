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
    Table 2:     Race
    Universe:    Total population
    Source code: B02001
    NHGIS code:  JMB
        JMBE001:     Total
        JMBE002:     White alone
        JMBE003:     Black or African American alone
        JMBE004:     American Indian and Alaska Native alone
        JMBE005:     Asian alone
        JMBE006:     Native Hawaiian and Other Pacific Islander alone
        JMBE007:     Some other race alone
        JMBE008:     Two or more races
        JMBE009:     Two or more races: Two races including Some other race
        JMBE010:     Two or more races: Two races excluding Some other race, and three or more races

"""
#TypeError: invalid type (<type 'str'>) for column ``total_mobility_pop``

if __name__ == '__main__':
    #map new fields to fields in NHGIS csv

    var_mapping={
        "total":"JMBE001"
        ,"mixrace":"JMBE008" 
        }

    raw="raw.csv"
    # TODO: convert(transpo_mapping,raw,outfilename, geoids=blkgrp_geoids)
    convert(var_mapping,raw,"mixrace")
