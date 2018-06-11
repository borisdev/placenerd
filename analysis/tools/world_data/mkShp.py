import pysal
wkt = pysal.open('world2.wkt','r')
shp = pysal.open('world.shp','w')
for p in wkt:
  shp.write(p)
shp.close()
