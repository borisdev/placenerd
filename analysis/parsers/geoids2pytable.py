"""NHGIS attribute values convert to a pyTable 
"""
import csv
import pysal
from tables import *

## SORT by shp index 

dbf = '/Users/slow/workspace/choropleth-maps/data/shapefiles/CA_blockgroup_2012/CA_blockgroup_2012.dbf'
def convert(dbf=dbf):

    # SAMPLE GEOID FROM DBF 06 071 000301 3
    #06 101 050503 5
    dbf = pysal.open(shapefiledbf)
    geoids = dbf.by_col('GEOID10') # shapefile geoid, 11chars=2state+3county+6tract
    N=len(geoids)

    class BlockModel(IsDescription):
        geoid      = StringCol(12)      
        shpidx     = UInt32Col()
        state      = StringCol(2)       
        county     = StringCol(3)       
        tract      = StringCol(6)       
        blkgrp     = StringCol(1)   

    inputfile=shapefiledbf.split("/")[-1].split(".")[0] # ordered geoids
    filename = inputfile + ".h5" # output

    # Extract geoids from our shapefile 
    id2idx=dict([(i[1],i[0]) for i in enumerate(geoids)])
    h5file = open_file(filename, mode = "w", title = "none")
    group = h5file.create_group("/", 'mygroup', 'mygroup')# new group above "/" (root)
    blocks = h5file.create_table(group, 'readout', BlockModel, "mytable")# new table of group

    for i,record in enumerate(reader):
        geoid=record[field["stateCode"]]+record[field["countyCode"]]+record[field["tractCode"]]+record[GEOFIELD]
        if geoid not in geoids:
            continue
        blocks.row['geoid']     = geoid
        blocks.row['shpidx']    = id2idx[geoid]

        blocks.row.append()
    h5file.close()


if __name__ == '__main__':
    pass
    #map new fields to fields in NHGIS csv
    #convert(var_mapping,raw,"transpo_mobility_schooling")
