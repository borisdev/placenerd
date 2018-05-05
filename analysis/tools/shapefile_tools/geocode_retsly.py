## Map Retsly MLS (Real Estate listings) on a choropleth of census tracts
from util import fast_geocoder
import time
from collections import deque
bg = 'data/2602F1384BA06F1C6F68E9A6676CDA1A.shp' # census tracts
import pysal
pysalshp = pysal.open(bg,'r') # finds what census area contains lat,lon
# fiona's filter() methods is a  1000x slower than charlies method
print "building locator...for getting potential areas containing points based on bbox"
t0 = time.time()
loc = fast_geocoder.BBoxLocator(bg)
t1 = time.time()
print "built locator in %0.2f seconds"%(t1-t0)
f = open('data/raw_data.csv','r') # lat, lon,...\n
o = open('tractids.csv','w')
header=f.next()
print header
t0 = time.time()
for idx, line in enumerate(f):
    linelist = line.strip().split(',')
    if linelist[0] =="lat": 
        continue
    y,x = map(float,[linelist[0],linelist[1]])
    thepoint=(x,y)
    return loc.area_contains_point(pt)
    print idx
t1 = time.time()
f.close()
o.close()

