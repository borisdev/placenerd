"""NHGIS attribute values convert to a pyTable 
"""
import csv
import pysal
from tables import *
import sys
sys.path.append("../../../../tools/parsers")
from nhgis2pytable import convert


if __name__ == '__main__':
    #map new fields to fields in NHGIS csv

    var_mapping={
        "income": "QWUE001"
        }

    raw="/Users/slow/workspace/geoscore/S3/attributes/usa_blockgroups/income/income.csv"
    convert(var_mapping,raw,"income")
