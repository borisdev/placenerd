import os
import autoreload
from dynTileMapper import mapTools
import fiona
shp="/home/ubuntu/geoscore/scripts/data/alaska.shp"
shp="/var/shapefiles/testing/6AEE65BA0099BDE214BB9686E55BE939.shp" # 2.1 GB
print shp

with fiona.open(shp, 'r') as source:
    N=len(source)
    print N
mapObj = mapTools.MapScriptObj(shp)
xml=shp.replace("shp","xml")
print xml
mapObj.save_to_mapfile(xml)

from dynTileMapper.tileMaker.tiler import Tiler
x = 0
y = 0
z = 0
border = False
png = Tiler(mapObj.mapObj).gTileDraw(x, y, z, border)
with open('raw_block_tile.png','w') as o:
    o.write(png)

from dynTileMapper.pypng import png
from dynTileMapper.pypng.optTile import optTile
raw = png.PNG(open('raw_block_tile.png','r'))
typ, dat = optTile(raw, encode=False) # encode, base64encode dat

from render import render,classification,colors
cl = classification.random(N,6) # create a random classification with 4 classes from N regions (6 = 4 classes + 1 background color + 1 border color)
cs = colors.ColorScheme([(0,0,1), (0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,128,0)])
png = render.overview(N, typ, dat, C = cl, CS = cs)
with open('final_block_tile.png','w') as o:
    o.write(png)

#### Step 4b. Render a colored Tile.
cs = colors.ColorScheme([(0,0,1), (0,0,0), (255,0,255), (128,255,0), (0,128,255), (0,128,0)])
png = render.overview(N, typ, dat, C = cl, CS = cs)
with open('final_block_tile2.png','w') as o:
    o.write(png)

