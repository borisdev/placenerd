"""NHGIS attribute values convert to a pyTable 

    Table 1:     Household Type (Including Living Alone)
    Universe:    Households
    Source code: B11001
    NHGIS code:  QTM
        QTME001:     Total
        QTME002:     Family households
        QTME003:     Family households: Married-couple family
        QTME004:     Family households: Other family
        QTME005:     Family households: Other family: Male householder, no wife present
        QTME006:     Family households: Other family: Female householder, no husband present
        QTME007:     Nonfamily households
        QTME008:     Nonfamily households: Householder living alone
        QTME009:     Nonfamily households: Householder not living alone
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
        "total":  "QTME001"
        ,"married":  "QTME003"
        ,"single_dad":  "QTME005"
        ,"single_mom":  "QTME006"
        ,"living_alone":  "QTME008"
        }

    raw="/Users/slow/workspace/geoscore/S3/attributes/usa_blockgroups/household_type/household_type.csv"
    convert(var_mapping,raw,"household_type")
