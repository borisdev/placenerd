"""NHGIS attribute values convert to a pyTable 
"""
import csv
import pysal
from tables import *
import sys
sys.path.append("../../../tools/parsers")
from nhgis2pytable import convert

## SORT by shp index 




if __name__ == '__main__':
    #map new fields to fields in NHGIS csv

    var_mapping={
        "total_transpo":"JM0E001"
        ,"drove_alone":"JM0E003" 
        ,"ferryboat":"JM0E015"    
        ,"motorbike":"JM0E017" 
        ,"bicycle":"JM0E018" # why so many 119s ? 
        ,"walked":"JM0E019" 
        ,"total_mobility":"JMLE001" 
        ,"diffMSA_mobility":"JMLE007" 
        ,"total_schooling":"JN9E001" 
        ,"MA_schooling":"JN9E033" 
        ,"selfemp_total":"JO7E001" 
        ,"selfemp":"JO7E002" 
        }

    # raw csv
    raw="/Users/slow/workspace/choropleth-maps/data/census_raw_tables/usa_blockgroups/boris_top_6.csv"
    #convert(new,raw)
    # TODO: convert(transpo_mapping,raw, geoids=blkgrp_geoids)
    convert(var_mapping,raw,"transpo_mobility_schooling")
