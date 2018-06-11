# Experimental code that create a PNG template without the need 
# of the intermediate step for writing anything to disk
# This method does NOT save anytime over Charlie'e method
# I am leaving the code here just in case I (Boris) need it for reference later

from dynTileMapper.pypng import png
from cStringIO import StringIO
from dynTileMapper.pypng.optTile import optTile
import mapnik
import os
import sys,os
sys.path.append('/usr/local/django')
os.environ['DJANGO_SETTINGS_MODULE']='gws_sqlite.settings'
from geodaWebServices.shapeManager.models import Shapefile
from geodaWebServices.dyntm.models import TileSet,Tile
from render import classification, render
from dynTileMapper.tileMaker.tiler import Tiler
import time
import numpy

#http://54.225.95.196/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=15&x=5719&y=13231

## SETUP  for render 1
tilesets= { 
             "ca_small":"dtmUser:E5DD7691F5A16482643A36C3794377E5" 
            ,"ca_blocks":"dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59" 
            ,"tx_blocks":"dtmUser:8AF4FAA7FD6BF0E2F28C24980EF84147"
            ,"part_usa":"dtmUser:59DC0A533A2710CCF56FF68ED44C3CFF" #3.3 GB
            ,"small_usa":"dtmUser:C3078238FE078071D273353909B6FE74" # 3 decimal precision  2.7 GB
          }

tsid=tilesets["ca_blocks"]
ts = TileSet.get_by_key_name(tsid)
shpfile = Shapefile.get_by_key_name(ts.shpfile)
mapfile=shpfile.map_path
tilerObj=Tiler(shpfile.map_path)
calc=tilerObj.calcExtent
#m=tilerObj.map

m = mapnik.Map(256,256)
mapnik.load_map(m, mapfile)


print" RENDER 1 -- by Mapnik "
i=0
times=[]
#for z in range(10,16):
for z in range(10,11):
    xmin,ymin,xmax,ymax=shpfile.gTileBounds(z)
    #for x in xrange(xmin,xmax+1):
    for x in range(xmin,xmin+1):
        #for y in xrange(ymin,ymax+1):
        for y in range(ymin,ymin+1):
            i=i+1

            tid = "u:%s:%d+%d+%d"%(ts.shpfile,z,x,y)
            print tid
            if z >10: 
                MAKEBORDER=True
            else:
                MAKEBORDER=False

            start=time.time()
            # CHARLIES METHOD
            #typ,dat = shpfile.raw_tile(x,y,z,border=MAKEBORDER)

            # CHARLIES METHOD BROKEN DOWN
            #f = open("temp.png","rw")
            #mapnik.render_to_file(m, f.name, "RGB24")
            #f.seek(0)
            #raw=f.read()
            #img = StringIO(raw)
            #f.close()
            #typ,dat = optTile(png.PNG(img),False)

            # NEW METHOD
            m.zoom_to_box(calc(x,y,z))
            im=mapnik.Image(256,256)
            mapnik.render(m, im)
            data = im.tostring('png')
            img = StringIO(data)
            typ,dat = optTile(png.PNG(img),False)

            end = time.time() - start
            times.append(end)

            tile = Tile(tid)
            tile.typ = typ
            tile.dat = str(dat)
            tile.put()
            print" zoom ,x,y count ",z,x,y, i

tarray=numpy.array(times)
print "max", tarray.max()
print "mean", tarray.mean()

png= render.overview(ts.numregions,typ,dat,width=256,height=256)
assert png!=None

## Validate it worked with your eyes
fname = 'NEWpart1-%s+%s+%s.png'%(z,x,y)
o = open('out/'+fname,'wb')
o.write(data)
o.close()
## Validate it worked with your eyes
fname = 'NEWpart2-%s+%s+%s.png'%(z,x,y)
o = open('out/'+fname,'wb')
o.write(png)
o.close()
