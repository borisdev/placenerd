# coding: utf-8
import os
import sys,os
sys.path.append('/usr/local/django')
os.environ['DJANGO_SETTINGS_MODULE']='gws_sqlite.settings'
from geodaWebServices.shapeManager.models import Shapefile
from geodaWebServices.dyntm.models import TileSet,Tile
from render import classification, render
import datetime

#http://54.225.95.196/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=15&x=5719&y=13231

## SETUP  for render 1
tilesets= { 
             "ca_small":"dtmUser:E5DD7691F5A16482643A36C3794377E5" 
            ,"ca_blocks":"dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59" 
            ,"tx_blocks":"dtmUser:8AF4FAA7FD6BF0E2F28C24980EF84147"
            ,"part_usa":"dtmUser:59DC0A533A2710CCF56FF68ED44C3CFF" #3.3 GB
            ,"small_usa":"dtmUser:C3078238FE078071D273353909B6FE74" # 3 decimal precision  2.7 GB
            ,"blkgrp": "dtmUser:80D72034643364302F8D513531046CDC"
          }

tsid=tilesets["blkgrp"]
ts = TileSet.get_by_key_name(tsid)
shpfile = Shapefile.get_by_key_name(ts.shpfile)


render1start=datetime.datetime.now()
print" RENDER 1 -- by Mapnik "
i=0
for z in range(0,16):
    xmin,ymin,xmax,ymax=shpfile.gTileBounds(z)
    for x in xrange(xmin,xmax+1):
        for y in xrange(ymin,ymax+1):
            i=i+1

            if z >10: 
                MAKEBORDER=True
            else:
                MAKEBORDER=False
            if MAKEBORDER:
                tid = "t:%s:%d+%d+%d"%(ts.shpfile,z,x,y)
            else:
                tid = "u:%s:%d+%d+%d"%(ts.shpfile,z,x,y)
            typ,dat = shpfile.raw_tile(x,y,z,border=MAKEBORDER)

            tile = Tile(tid)
            tile.typ = typ
            tile.dat = str(dat)
            tile.put()
            print" zoom ,x,y count ",z,x,y, i
            render1end=datetime.datetime.now()
            d1=render1end-render1start
            print d1.seconds, "time seconds elapsed"

