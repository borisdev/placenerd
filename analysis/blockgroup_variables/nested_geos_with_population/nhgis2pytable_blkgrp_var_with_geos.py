"""NHGIS attribute values convert to a pyTable 
"""
import csv
import pysal
from tables import *

## SORT by shp index 

def convert(fieldmapping,raw,outfilename):
    """
    #map new fields to fields in NHGIS csv
    new={
        "total_vacant"  :"MTEE001"
        ,"for_rent"     :"MTEE002" 
        ,"for_sale"     :"MTEE004"    
        ,"other_vacant" :"MTEE008" 
        ,"total_own"    :"MU6E001" 
        ,"total_rent"   :"MUTE001" 
        }

    # raw csv
    raw="/Users/slow/workspace/choropleth-maps/data/raw/nhgis/ca_blockgroups/housing.csv"
    convert(new,raw,"MY_OUTPUT")
    """

    #shapefiledbf = '/Users/slow/workspace/choropleth-maps/data/shapefiles/CA_blockgroup_2012/CA_blockgroup_2012.dbf'
    shapefiledbf = '/Users/slow/workspace/choropleth-maps/data/shapefiles/USA_blck_grp/US_blck_grp_2010.dbf'
    GEOFIELD="BLKGRPA"

    class BlockModel(IsDescription):
        shpidx     = UInt32Col()     # shapefile geoid index position
        geoid      = StringCol(16)   # 16-character String)    
        stateName      = StringCol(16)   # 16-character String)    
        countyName      = StringCol(16)   # 16-character String)    
        placeName      = StringCol(16)   # 16-character String)    
        msaName        = StringCol(16)   # 16-character String)    
        stateCode      = StringCol(16)   # 16-character String)    
        countyCode      = StringCol(16)   # 16-character String)    
        placeCode      = StringCol(16)   # 16-character String)    
        msaCode        = StringCol(16)   # 16-character String)    

    for newfield in fieldmapping.keys():
        BlockModel.columns[newfield] = UInt32Col()     

    # set output pytable file name 
    attribute=raw.split("/")[-1].split(".")[0]
    geometry=shapefiledbf.split("/")[-1].split(".")[0] # ordered geoids
    #filename = geometry + "_" + attribute + ".h5" # output
    filename = outfilename + ".h5" # output

    reader = csv.DictReader(open(raw,"rb"))
    #print reader.fieldnames

    # Extract geoids from our shapefile 
    dbf = pysal.open(shapefiledbf)
    #geoids = dbf.by_col('GEOID') # shapefile geoid, 11chars=2state+3county+6tract
    geoids = dbf.by_col('GEOID10') # shapefile geoid, 11chars=2state+3county+6tract
    id2idx=dict([(i[1],i[0]) for i in enumerate(geoids)])
    N=len(geoids)
    h5file = open_file(filename, mode = "w", title = "none")
    group = h5file.create_group("/", 'mygroup', 'mygroup')# new group above "/" (root)
    blocks = h5file.create_table(group, 'readout', BlockModel, "mytable")# new table of group
    import time
    s=time.time() 
    field={
        "gisjoin" :"GISJOIN"
        ,"stateName" :"STATE"
        ,"stateCode" :"STATEA"
        ,"countyName":"COUNTY"
        ,"countyCode":"COUNTYA"
        ,"placeName" :"PLACE"
        ,"placeCode" :"PLACEA"
        ,"tractCode" :"TRACTA"
        ,"msaName" :"CBSA"
        ,"msaCode" :"CBSAA"
        }

    for i,record in enumerate(reader):
        geoid=record[field["stateCode"]]+record[field["countyCode"]]+record[field["tractCode"]]+record[GEOFIELD]
        if geoid not in geoids:
            continue
        blocks.row['geoid']     = geoid
        blocks.row['shpidx']    = id2idx[geoid]
        blocks.row['stateName']    = record[field['stateName']]
        blocks.row['stateCode']    = record[field['stateCode']]
        blocks.row['countyName']    = record[field['countyName']]
        blocks.row['countyCode']    = record[field['countyCode']]
        blocks.row['placeName']    = record[field['placeName']]
        blocks.row['placeCode']    = record[field['placeCode']]
        blocks.row['msaName']    = record[field['msaName']]
        blocks.row['msaCode']    = record[field['msaCode']]

        kvlist=fieldmapping.items()
        for newfield ,nhgisfield in kvlist:
            #print record[nhgisfield]
            #invalid type (<type 'str'>) for column ``total_mobility``
            blocks.row[newfield]     = record[nhgisfield]
        #print blocks.row
        blocks.row.append()
        if i % 100 ==0: 
            print i ," of ", N
            print "seconds: ", time.time() - s
        #if i==10: break
    h5file.close()


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
