"""NHGIS attribute values convert to a pyTable 
"""
import csv
import pysal


if __name__ == '__main__':
    raw="raw.csv"
    reader = csv.DictReader(open(raw,"rb"))
    print reader.fieldnames
    for i,record in enumerate(reader):
            #invalid type (<type 'str'>) for column ``total_mobility``
            if record['STATEA']!='72':
                try:
                    type(int(record["JMLE001"]))
                except:
                    print record
                    print i, "raw: ", repr(record["JMLE001"])
                    print i, "int: ", int(record["JMLE001"])
                    print i, "type: ", type(int(record["JMLE001"]))
                else:
                    print i


