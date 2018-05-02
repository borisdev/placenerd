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
    Universe:    Population 1 year and over living in a Metropolitan Statistical Area in the United States
        JMLE001:     Total
        JMLE002:     Same house 1 year ago
        JMLE007:     Different house in United States 1 year ago: Different Metropolitan Statistical Area
        JMLE012:     Abroad 1 year ago
"""
#TypeError: invalid type (<type 'str'>) for column ``total_mobility_pop``

if __name__ == '__main__':
    #map new fields to fields in NHGIS csv

    var_mapping={
        "total_mobility_pop":"JMLE001"
        ,"same_house_last_year":"JMLE002" 
        ,"diff_usamsa_last_year":"JMLE007"    
        ,"abroad_last_year":"JMLE012" 
        }

    raw="raw.csv"
    # TODO: convert(transpo_mapping,raw,outfilename, geoids=blkgrp_geoids)
    convert(var_mapping,raw,"mobility")
