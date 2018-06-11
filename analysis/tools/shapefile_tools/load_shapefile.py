import sys
sys.path.append("../src/pyClient")
sys.path.append("../../dynTM/src/pyClient")
import sys
import DynTM # make stand alone client-loader?
import random
import csv
f1="/mnt/merge_ca_ct_rest/blocks_minus_ca_ct/merged_blocks_final.shp"
f2="/mnt/merge_ca_ct_rest/blocks_minus_ca_ct/merged_blocks_final.shx"

f1="/Users/slow/workspace/choropleth-maps/data/shapefiles/CA_blockgroup_2012/CA_blockgroup_2012.shp"
f2="/Users/slow/workspace/choropleth-maps/data/shapefiles/CA_blockgroup_2012/CA_blockgroup_2012.shx"

f1="../../S3/shapefiles/USA_blockgroup_2010/US_blck_grp_2010.shp"
f2="../../S3/shapefiles/USA_blockgroup_2010/US_blck_grp_2010.shx"


AccessKeyID = 'dtmUser'
AccessKey = 'key'
border = False
client=DynTM.GeoDaWS_DynTM(AccessKeyID=AccessKeyID,AccessKey=AccessKey)

with open(f1,'rb') as shp:
    with open(f2,'rb') as shx:
        tileset_id = client.createTileSet(shp, shx)
print "DONE WITH BLOCKS!!"
print "Tileset ID:",tileset_id



number_of_regions = client.describeTileSet(tileset_id)['numregions']
print "number_of_regions: ", number_of_regions

# tile coordinates to display USA's southeast
z=3
x=2
y=3 

png = client.getTile(tileset_id, z, x, y)
print ""
print ""
print ""
print " *** JavaScript Map URL Parameters *** "
print ""
print "var TILESET='"+tileset_id+"'"
