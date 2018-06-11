"""
TODO: makes this for CLI
load color schemes and classification lists into geoscores database
"""

import sys
sys.path.append("~/workspace/geoscore/src/pyClient")
import DynTM # make stand alone client-loader?
import random
import csv
# TODO: Make singleton class to handle repeated I/O and common data 
# TODO: errror handling for 500 and 404
# TODO: tests to make sure all server components in working order
# TODO: db.loadtileset()
# TODO: db.loadclasslist() 
# TODO: db.loadcolorscheme()
# TODO: map parameters as a YAML or JSON
# TODO: preload all colorbrewer data
# TODO: preload all census geometries

#f="census/output_classlists/majorities_classlist.csv"
f="percent_poor.csv"
with open(f,'rb') as csvfile:
    CLASSLIST = [ int(line.strip()) for line in csvfile.readlines()]
GEOMETRY="ca_blockgroup"
AccessKeyID = 'dtmUser'
AccessKey = 'key'
border = False
client=DynTM.GeoDaWS_DynTM(AccessKeyID=AccessKeyID,AccessKey=AccessKey)

tileset_ids={ "tract": "dtmUser:2602F1384BA06F1C6F68E9A6676CDA1A",
              "ca_blockgroup":'dtmUser:F79F21D4E1C847A6B0CD19E4D1E20892',
              "blockgroup": None,
              "block": None}
tileset_id=tileset_ids[GEOMETRY]

#with open('/pyacs/tracts11.shp','rb') as shp:
#    with open('/pyacs/tracts11.shx','rb') as shx:
#        tileset_id = client.createTileSet(shp, shx)

print "Tileset ID:",tileset_id

# tile coordinates to display USA's southeast
z=3
x=2
y=3 

Nclasses=len(CLASSLIST)
number_of_regions = client.describeTileSet(tileset_id)['numregions']
assert Nclasses==number_of_regions, "Error: Shapefile and classlist must be same length: %r" % Nclasses


# perhaps in future pre-load all of color brewer??
# #810F7C dynTM cant handle this color http://colorbrewer2.org/ 5 BuPu sequential
#colors=['#EDF8FB', '#B3CDE3', '#8C96C6', '#8856A7', '#4D004B']

# 10 colors  PuRd
colors=[ "#0xF7F4F9",
         "0xE7E1EF",
         "0xD4B9DA",
         "0xC994C7",
         "0xDF65B0",
         "0xE7298A",
         "#0xCE1256",
         "#0x980043",
         "#0x67001F",
         "#0x67001F"]#10 Rd

classes=set(CLASSLIST) # extract the set of unique classes/numbers
# zero is transperant and is already defined
if 0 in classes: classes.remove(0)
Nuniqueclasses = len(classes)
print "classes: ", Nuniqueclasses
print "colors: ", len(colors)
# assert len(colors)==Nuniqueclasses, "Error: Unique classifications != colors"

classification_id = client.createClassification(tileset_id, CLASSLIST)
scheme_id = client.createColorScheme(colors)

png = client.getTile(tileset_id, z, x, y, classification_id, scheme_id,border)
print ""
print ""
print ""
print " *** JavaScript Map URL Parameters *** "
print ""
print "var TILESET='"+tileset_id+"'"
print "var CLASSIFICATION='"+classification_id+"'" 
print "var SCHEME='"+scheme_id+"'" 
