import pysal
import simplejson
import numpy
shapefiledbf = '/Users/slow/workspace/choropleth-maps/data/shapefiles/USA_blck_grp/US_blck_grp_2010.dbf'
dbf = pysal.open(shapefiledbf)
geoids = dbf.by_col('GEOID10')
N=len(geoids)
print "count: ", N

data=simplejson.dumps(geoids)
f=open("geoids.json","w")
f.write(data)
f.close()

numpy.save("dbf_geoids.npy", numpy.array(geoids))

