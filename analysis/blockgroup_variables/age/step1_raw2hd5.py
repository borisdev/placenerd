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
    #Table 1:     Sex by Age
    #Universe:    Total population
    #Source code: B01001
    #NHGIS code:  QSE

    #map new fields to fields in NHGIS csv

    var_mapping={
          "total":          "QSEE001"#     Total
         ,"Male" :          "QSEE002"#     Male
         ,"MaleUnder5":     "QSEE003"#     Male: Under 5 years
         ,"Male5to9"  :     "QSEE004"#     Male: 5 to 9 years
         ,"Male10to14":     "QSEE005"#     Male: 10 to 14 years
         ,"Male15to17":     "QSEE006"#     Male: 15 to 17 years
         ,"Male18to19":     "QSEE007"#     Male: 18 and 19 years
         ,"Male20"    :     "QSEE008"#     Male: 20 years
         ,"Male21"    :     "QSEE009"#     Male: 21 years
         ,"Male22to24":     "QSEE010"#     Male: 22 to 24 years
         ,"Male25to29":     "QSEE011"#     Male: 25 to 29 years
         ,"Male30to34":     "QSEE012"#     Male: 30 to 34 years
         ,"Male35to39":     "QSEE013"#     Male: 35 to 39 years
         ,"Male40to44":     "QSEE014"#     Male: 40 to 44 years
         ,"Male45to49":     "QSEE015"#     Male: 45 to 49 years
         ,"Male50to54":     "QSEE016"#     Male: 50 to 54 years
         ,"Male55to59":     "QSEE017"#     Male: 55 to 59 years
         ,"Male60and61":    "QSEE018"#     Male: 60 and 61 years
         ,"Male62to64":     "QSEE019"#     Male: 62 to 64 years
         ,"Male65and66":    "QSEE020"#     Male: 65 and 66 years
         ,"Male67to69":     "QSEE021"#     Male: 67 to 69 years
         ,"Male70to74":     "QSEE022"#     Male: 70 to 74 years
         ,"Male75to79":     "QSEE023"#     Male: 75 to 79 years
         ,"Male80to84":     "QSEE024"#     Male: 80 to 84 years
         ,"Male85over":     "QSEE025"#     Male: 85 years and over
         ,"Female"    :    "QSEE026"#     Female
         ,"FemaleUnder5"   :"QSEE027"#     Female: Under 5 years
         ,"Female5to9"     :"QSEE028"#     Female: 5 to 9 years
         ,"Female10to14"   :"QSEE029"#     Female: 10 to 14 years
         ,"Female15to17"   :"QSEE030"#     Female: 15 to 17 years
         ,"Female18and19"  :"QSEE031"#     Female: 18 and 19 years
         ,"Female20"       :"QSEE032"#     Female: 20 years
         ,"Female21"       :"QSEE033"#     Female: 21 years
         ,"Female22to24"   :"QSEE034"#     Female: 22 to 24 years
         ,"Female25to29"   :"QSEE035"#     Female: 25 to 29 years
         ,"Female30to34"   :"QSEE036"#     Female: 30 to 34 years
         ,"Female35to39"   :"QSEE037"#     Female: 35 to 39 years
         ,"Female40to44"   :"QSEE038"#     Female: 40 to 44 years
         ,"Female45to49"   :"QSEE039"#     Female: 45 to 49 years
         ,"Female50to54"   :"QSEE040"#     Female: 50 to 54 years
         ,"Female55to59"   :"QSEE041"#     Female: 55 to 59 years
         ,"Female60and61"  :"QSEE042"#     Female: 60 and 61 years
         ,"Female62to64"   :"QSEE043"#     Female: 62 to 64 years
         ,"Female65and66"  :"QSEE044"#     Female: 65 and 66 years
         ,"Female67to69"   :"QSEE045"#     Female: 67 to 69 years
         ,"Female70to74"   :"QSEE046"#     Female: 70 to 74 years
         ,"Female75to79"   :"QSEE047"#     Female: 75 to 79 years
         ,"Female80to84"   :"QSEE048"#     Female: 80 to 84 years
         ,"Female85over":"QSEE049"#     Female: 85 years and over
                        }

    raw="/Users/slow/workspace/geoscore/S3/attributes/usa_blockgroups/age/age.csv"
    convert(var_mapping,raw,"age")
