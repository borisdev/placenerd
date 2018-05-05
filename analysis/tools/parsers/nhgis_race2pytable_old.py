"""Extract and store census tract data from NHGIS as a pyTable 

    As a pyTable its easier to work with census variables using numpy

    TODO: compare race to metro area instead of county: http://en.wikipedia.org/wiki/Core_Based_Statistical_Area 955
"""
import csv
import pysal
from tables import *
#import numpy
#import pyACS

field={
 "gisjoin"    :"GISJOIN"     
 ,"total"     :"H7V001"      
 ,"totalRace" :"H7X001"      
 ,"white"     :"H7X002"      
 ,"black"     :"H7X003"      
 ,"native"    :"H7X004"      
 ,"asian"     :"H7X005"      
 ,"pacific"   :"H7X006"      
 ,"other"     :"H7X007"      
 ,"mixed"     :"H7X008"      
 ,"stateName" :"STATE"       
 ,"stateCode" :"STATEA"      
 ,"countyName":"COUNTY"      
 ,"countyCode":"COUNTYA"     
 ,"placeName" :"PLACE"       
 ,"placeCode" :"PLACEA"      
 ,"tractCode" :"TRACTA"      
 ,"blockCode" :"BLOCKA"      
 ,"msaName"   :"CBSA"      
 ,"msaCode"   :"CBSAA"      
 }

reader = csv.DictReader(open("input_census_data/nhgis_ca_blocks.csv","rb"))
print reader.fieldnames


def profile_NNGIS_table(reader):
    blockssame=[]
    blockszero=[]
    for record in reader:
        blockszero.append(record[field["total"]]=='0')
        blockssame.append(record[field["total"]]==record[field["totalRace"]])
    # 43 percent of ca blocks have popultion reported as zero?
    # wiki also says about same: http://en.wikipedia.org/wiki/Census_block
    print "Zero population blocks: ", sum(blockszero)/len(blockssame)*1.0
    print "Total and Total Race are same: ",sum(blockssame)/len(blockssame)*1.0

def nhgis2census(x):
    """ convert NHGIS's strange geoid to census format geoid 

    Census shapefile geoid is 15 chars = 2 state + 3 county + 6 tract + 4 block

    NHGHIS GISJOIN is 18 chars = "G" + 2 state + "0" + 3 county + "0" + 6 tract + 4 block

    from GSIJOIN remove extra characters: "G", and "0"s located before and after county

        POPOUT:  -++-+++-++++++++++
        EXAMPLE: G06007300085011009
    """
    st=x[1:3] 
    county=x[4:7] 
    tractblock=x[8:]
    return st+county+tractblock

def profile_geoids_nhgis_and_shapefile(reader,geoids):
    geoids_nhgis=[]
    for record in reader:
        geoids_nhgis.append(nhgis2census(record[field["GISJOIN"]]))
        print len(set(geoids).difference(set(geoids_nhgis)))
        #Out: 8321
        print len(set(geoids_nhgis).difference(set(geoids)))
        #Out: 5120
        # WHY is NHGIS missing 8321 blocks
        print "count in our shapefile ", len(geoids)
        #Out: 713346
        print "count in NHGIS ", len(geoids_nhgis)
        #Out[28]: 710145

    geoids_nhgis=[]
    for i,record in enumerate(reader):
        geoids_nhgis.append(record[field["stateCode"]]+record[field["countyCode"]]+record[field["tractCode"]]+record[field["blockCode"]])

    print len(set(geoids).difference(set(geoids_nhgis)))
    print len(set(geoids_nhgis).difference(set(geoids)))
    print "count in our shapefile ", len(geoids)
    print "count in NHGIS ", len(geoids_nhgis)

# Extract geoids from our shapefile 
dbf = pysal.open('input_census_data/CA_blocks.dbf')
geoids = dbf.by_col('GEOID') # shapefile geoid, 11chars=2state+3county+6tract

id2idx=dict([(i[1],i[0]) for i in enumerate(geoids)])

# Define pyTable of census block records
# UInt16Col is an Unsigned short integer
class BlockModel(IsDescription):
    geoid      = StringCol(16)   # 16-character String)    
    shpidx     = UInt32Col()     # shapefile geoid index position
    total      = UInt32Col()     # total
    black      = UInt32Col()    
    white      = UInt32Col()     
    native     = UInt32Col()   
    asian      = UInt32Col()   
    mixed      = UInt32Col() 

N=len(geoids)
filename = "ca_blocks.h5" 
h5file = open_file(filename, mode = "w", title = "shpidx CA_blocks.shp, NHGIS ca blocks")
group = h5file.create_group("/", 'race', 'race')# new group under "/" (root)
blocks = h5file.create_table(group, 'readout', BlockModel, "Race Counts")# new table of group
import time
s=time.time() 

for i,record in enumerate(reader):
    #geoid=nhgis2census(record["GISJOIN"])
    geoid=record[field["stateCode"]]+record[field["countyCode"]]+record[field["tractCode"]]+record[field["blockCode"]]
    if geoid not in geoids:
        continue
    blocks.row['geoid']     = geoid
    blocks.row['shpidx']    = id2idx[geoid]
    blocks.row['total']     = record[field["total"]]
    blocks.row['black']     = record[field["black"]]
    blocks.row['white']     = record[field["white"]]
    blocks.row['native']    = record[field["native"]]
    blocks.row['asian']     = record[field["asian"]]
    blocks.row['mixed']     = record[field["mixed"]]
    #print blocks.row
    blocks.row.append()
    if i % 100 ==0: 
        print i ," of ", N
        print time.time() - s
    #if i==10: break

# Close (and flush) the file
h5file.close()
