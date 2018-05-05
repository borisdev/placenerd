#https://github.com/mapnik/mapnik/wiki/GettingStartedInPython
import pysal
db = pysal.open('data/world.dbf')
colors = db.by_col('dtmValue') #['#000002', '#000003', '#000004', '#000005']

import mapnik

m = mapnik.Map(600,300) # create a map with a given width and height in pixels
# note: m.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
# the 'map.srs' is the target projection of the map and can be whatever you wish 
m.srs = '+init=epsg:3857'
#m.background = mapnik.Color('steelblue') # set background colour to 'steelblue'.  


s = mapnik.Style() # style object to hold rules
for color in colors:
	r = mapnik.Rule() # rule object to hold symbolizers
	# to fill a polygon we create a PolygonSymbolizer
	r.filter = mapnik.Filter('[dtmValue]="%s"'%color)
	polygon_symbolizer = mapnik.PolygonSymbolizer(mapnik.Color(color))
	r.symbols.append(polygon_symbolizer) # add the symbolizer to the rule object
	# to add outlines to a polygon we create a LineSymbolizer
	line_symbolizer = mapnik.LineSymbolizer(mapnik.Color('rgb(100%,0%,0%)'),1)
	r.symbols.append(line_symbolizer) # add the symbolizer to the rule object
	s.rules.append(r) # now add the rule to the style and we're done

m.append_style('My Style',s) # Styles are given names only as they are applied to the map

ds = mapnik.Shapefile(file='data/world.shp')

layer = mapnik.Layer('world')
layer.datasource = ds
layer.styles.append('My Style')

m.layers.append(layer)
m.zoom_all()

mapnik.render_to_file(m,'world.png', 'RGB24')
