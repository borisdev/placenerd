#### Step 0. Copy shapefiles to working location (assume they were uploaded)
import os
if not os.path.exists('output'):
    os.mkdir('output')
with open('data/world.shp','r') as i:
    with open('output/world.shp', 'w') as o:
        o.write(i.read())
with open('data/world.shx','r') as i:
    with open('output/world.shx', 'w') as o:
        o.write(i.read())
#### Step 1. Create a Mapnik Mapfile
## remember to run$ python  dynTileMapper/setup.py install
from dynTileMapper import mapTools

mapObj = mapTools.MapScriptObj('output/world.shp')
mapObj.save_to_mapfile('output/world.xml')

#### Step 2. Create a "raw" tile.
from dynTileMapper.tileMaker.tiler import Tiler
x = 0
y = 0
z = 0
border = False
#png = Tiler('world.xml').gTileDraw(x, y, z, border)
png = Tiler(mapObj.mapObj).gTileDraw(x, y, z, border)
with open('output/raw_tile.png','w') as o:
    o.write(png)

#### Step 3. Optimize raw tile
####    Yields one for 4 types,
####    A - Blank -- requested tile outside bounds of shapefile
####    B - Single Color -- zoomed in so far that this tile is fully contained inside one polygon
####    C - Raster Tile -- more then 254 regions contained in the tile, PNG spec does not allow more
####                       colors to be represented in the palette, each cell in the raster be updated.
####    D - PLTE Tile -- Tile contains fewer than 254 regions and can be recolor by changing colors
####                     in the color palette only
from dynTileMapper.pypng import png
from dynTileMapper.pypng.optTile import optTile
raw = png.PNG(open('output/raw_tile.png','r'))
typ, dat = optTile(raw, encode=False) # encode, base64encode dat

#### Step 4. Render a colored Tile.
import pysal
from render import render,classification,colors
shp = pysal.open('data/world.shp','r')
N = len(shp) # number of regions
cl = classification.random(N,6) # create a random classification with 4 classes from N regions (6 = 4 classes + 1 background color + 1 border color)
cs = colors.ColorScheme([(0,0,1), (0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,128,0)])
png = render.overview(N, typ, dat, C = cl, CS = cs)
with open('output/tile.png','w') as o:
    o.write(png)

#### Step 4b. Render a colored Tile.
cs = colors.ColorScheme([(0,0,1), (0,0,0), (255,0,255), (128,255,0), (0,128,255), (0,128,0)])
png = render.overview(N, typ, dat, C = cl, CS = cs)
with open('output/tile2.png','w') as o:
    o.write(png)

