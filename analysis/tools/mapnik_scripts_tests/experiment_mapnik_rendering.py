# coding: utf-8
from dynTileMapper.pypng import png
from dynTileMapper.pypng.optTile import optTile
from cStringIO import StringIO
import os
import sys,os
sys.path.append('/usr/local/django')
os.environ['DJANGO_SETTINGS_MODULE']='gws_sqlite.settings'
from geodaWebServices.shapeManager.models import Shapefile
from geodaWebServices.dyntm.models import TileSet,Tile
from render import classification, render
import time
from dynTileMapper.tileMaker.tiler import Tiler
import mapnik
import numpy
times=[]
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
start=time.time()
#for z in range(0,16):
for z in range(10,17):
    xmin,ymin,xmax,ymax=shpfile.gTileBounds(z)
    for x in xrange(xmin,xmax+1):
    #for x in range(xmin,xmin+1):
        for y in xrange(ymin,ymax+1):
        #for y in range(ymin,ymin+1):
            i=i+1

            tid = "u:%s:%d+%d+%d"%(ts.shpfile,z,x,y)
            if z >10: 
                MAKEBORDER=True
            else:
                MAKEBORDER=False
            #start=time.time()
            # CHARLIES METHOD BROKEN DOWN
            f = open("temp.png","rw")
            m.zoom_to_box(calc(x,y,z))
            mapnik.render_to_file(m, f.name, "RGB24")
            f.seek(0)
            img = StringIO(f.read())
            f.close()
            typ,dat = optTile(png.PNG(img),False)
            del img
            end = time.time() - start
            times.append(end)

            tile = Tile(tid)
            tile.typ = typ
            tile.dat = str(dat)
            tile.put()
            del tile
            del typ
            del dat
            print time.time()-start
            print" zoom ,x,y count ",z,x,y, i
#tarray=numpy.array(times)
#print "max", tarray.max()
#print "mean", tarray.mean()

#png= render.overview(ts.numregions,typ,dat,width=256,height=256)
#assert png!=None

#verify with  your eyes
#fname = 'NEW2part2-%s+%s+%s.png'%(z,x,y)
#o = open('out/'+fname,'wb')
#o.write(png)
#o.close()
