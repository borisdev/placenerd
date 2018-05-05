""" wrapper for topojson.js
Make topojson from shapefiles:

input_filenames = [
    "shapefiles/hispaniola_boundaries/Hispaniola_Admin_Boundaries.shp",
    "shapefiles/hispaniola_boundaries/Hispaniola_Country_Boundaries.shp"
    ]
shp2topojson(input_filenames, output_filename='temp_topo.json', zoom=16)



"""
import urllib
import fiona
from itertools import chain
import json
import subprocess
import os
import sys
import datetime
import shlex
from math import radians, cos, sin, asin, sqrt
from pysal import rook_from_shapefile as neighbors

# $which topojson
# edit this command path 
#TOPOJSON='/usr/local/share/npm/bin/topojson' # Boris laptop 
#TOPOJSON='topojson' 
#TOPOJSON='/usr/local/bin/topojson' # Big AWS machine named topojson-boris
TOPOJSON='/usr/bin/topojson' # Big AWS machine named topojson-boris
TEMP_FILE="topojson_simplified_temporary_file.json"

def rel2abs(arc, scale=None, translate=None):
    """Yields absolute coordinate tuples from a delta-encoded arc.

    If either the scale or translate parameter evaluate to False, yield the
    arc coordinates with no transformation."""
    if scale and translate:
        a, b = 0, 0
        for ax, bx in arc:
            a += ax
            b += bx
            yield scale[0]*a + translate[0], scale[1]*b + translate[1]
    else:
        for x, y in arc:
            yield x, y

def arcs2coordinates(arcs, topology_arcs, scale=None, translate=None):
    """Return GeoJSON coordinates for the sequence(s) of arcs.
    
    The arcs parameter may be a sequence of ints, each the index of a
    coordinate sequence within topology_arcs
    within the entire topology -- describing a line string, a sequence of 
    such sequences -- describing a polygon, or a sequence of polygon arcs.
    
    The topology_arcs parameter is a list of the shared, absolute or
    delta-encoded arcs in the dataset.

    The scale and translate parameters are used to convert from delta-encoded
    to absolute coordinates. They are 2-tuples and are usually provided by
    a TopoJSON dataset. 
    """
    if isinstance(arcs[0], int):
        coords = [
            list(
                rel2abs(
                    topology_arcs[arc if arc >= 0 else ~arc],
                    scale, 
                    translate )
                 )[::arc >= 0 or -1][i > 0:] \
            for i, arc in enumerate(arcs) ]
        return list(chain.from_iterable(coords))
    elif isinstance(arcs[0], (list, tuple)):
        return list(
            arcs2coordinates(arc, topology_arcs, scale, translate) for arc in arcs)
    else:
        raise ValueError("Invalid input %s", arcs)

def get_meta_properties_dict(shapefile):
    """    
        >>> shapefile="shapefiles/counties/tl_2012_us_county.shp"
        >>> properties=make_properties_dict(shapefile)
        >>> print properties["1"]
        >>> del properties
    """
    meta={}
    with fiona.collection(shapefile, 'r') as source:
        meta['schema']=source.schema
        meta['crs']=source.crs
        meta['driver']=source.driver.encode('ascii','ignore')
        properties=dict([(rec['id'],rec['properties']) for rec in source])
        return meta, properties 

def topojson2shapefiles(shapefiles, topojsonfile):
    """One simplified topojson back to many shapefiles"""
    topojson=topojsonfile
    json_file = open(topojson,"r")
    data = json_file.read()
    json_file.close()
    topology = json.loads(data)
    scale = topology['transform']['scale']
    translate = topology['transform']['translate']
    arcs = topology['arcs']

    for f in shapefiles:

        meta, propertiesDict = get_meta_properties_dict(f)

        newfilename=f.replace('.shp', '_simplified.shp')

        neighborsDict = neighbors(f) # contiguity structure of shapefile

        with fiona.collection(newfilename, 'w', **meta) as sink:


            print "Creating: ", newfilename

            # translate topojson arcs for each state into geojson type dict

            shapefile=f.replace('.shp',"").split("/")[-1] # remove suffix and directories
            print shapefile
            print topology['objects'].keys()
            for idx,obj in enumerate(topology['objects'][shapefile]['geometries']):
                #print idx,obj
                if obj['type'] == None:
                    #print "** Warning: ",shapefile,idx, '{"type:Null"}'
                    #print obj
                    if len(neighborsDict[idx])!=0:
                        print "Dropping a shape with neighbors!"
                        print neighborsDict[idx]
                        sys.exit()
                elif len(obj['arcs'])==0:
                    #print "** Warning: ", shapefile,idx, "has no arcs"
                    #print obj
                    if len(neighborsDict[idx])!=0:
                        print "Dropping a shape with neighbors!"
                        print neighborsDict[idx]
                        sys.exit()
                else:
                    coordinates=arcs2coordinates(obj['arcs'], arcs, scale,translate)
                    sink.write({
                            "id":idx,
                            "geometry":{"type": obj['type'],"coordinates":coordinates},
                            "properties": propertiesDict[str(idx)]
                            })
            del propertiesDict
            del meta


def test_clean_shapefiles(filenames):
    for f in filenames:    
        with fiona.collection(f, "r") as source:
            print "source.name: ", source.name
            print "source.meta: ", source.meta
            s=list(source)
            print "record length: ",len(s)
            print "-------------------------"
            for x in s:
                if x['geometry']['type']!='Polygon' and x['geometry']['type']!='MultiPolygon': 
                    print "problem: ", x['geometry']['type']
                    break


def distance(lon1, lat1, lon2, lat2):
    """
    haversine formula: stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points

    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km * 10**3 

def max_dimension(shapefile):
    # getting bounds
    print "shapefile: ", shapefile
    with fiona.collection(shapefile, 'r') as source:
        print shapefile
        west=source.bounds[0] 
        south=source.bounds[1] 
        east=source.bounds[2] 
        north=source.bounds[3]

    east_west_dist = distance(west, 0, east, 0) # at equator
    north_south_dist = distance(0, north, 0, south)
    return max(east_west_dist , north_south_dist)

class MapScale(object):
    # Given: 1 steradian is approx 40  million km-sqr out of 510 million km-sqr of Earth
    # Validate `meters_per_pixel` against http://wiki.openstreetmap.org/wiki/Zoom_levels

    meter_area_earth = 510 * (10**9)  
    sphere_steradian_ratio = 1/12.57
    meter_length_equator = 40*10**6
    meter_area_one_earth_steradian = meter_area_earth * sphere_steradian_ratio

    def __init__(self,zoom,shapefiles):
        #self.z = max(0, zoom + 3) # fudge factor...put in zoom 16, we treat it like zoom 19 (because maybe our initial math is off?)
        self.z = max(0, zoom ) # fudge factor...put in zoom 16, we treat it like zoom 19 (because maybe our initial math is off?)
        self.pixel_length_equator = 256.0 * 2**self.z # number of pixels to represent the equator
        self.meters_per_pixel = (self.meter_length_equator / self.pixel_length_equator)

        ## Steradians parameter
        # OLD # self.steradian_per_pixel = self.meters_per_pixel / self.meter_area_one_earth_steradian
        #NEW 
        self.steradian_per_pixel = (self.meters_per_pixel**2) / self.meter_area_one_earth_steradian


        ## Quantization parameter
        
        if type(shapefiles)==type([]):# a list of files
            self.max_dimension = max([ max_dimension(shp) for shp in shapefiles])
        else: # just one shapefile
            self.max_dimension = max_dimension(shapefiles)
        self.max_pixel_length = self.max_dimension / self.meters_per_pixel

        #print "TEST should be close to 40 * 10**9: ", self.meter_area_one_earth_steradian 
        print "max_dimension meters ", int(self.max_dimension) 
        print "max_pixel_length  ", int(self.max_pixel_length) 
        print "pixels of equator  ", int(self.pixel_length_equator)


    def __repr__(self):
        return 'MapScale(zoom={},meters_of_1pixel={},steradians_of_1pixel={})'.format(
            self.z
            ,self.meters_per_pixel
            ,self.steradian_per_pixel)



def shp2topojson(input_filenames, output_filename=TEMP_FILE, zoom=16, pixel_distort=0):
    """
        - inputfiles, list of shapefiles 
        - topojsonfile, a temporary topojson file 

        steradian="1e-12", removes triangle areas the size of a small apartment
        quantization="1e7", pixel circumferance of earth at zoom 15

         old at zoom 16 steradians='1e-12'(1+pixel_distort) 
    """
    scale=MapScale(zoom, input_filenames)
    print scale
    print "~~~~~~~~~~~~~~~~~~~~~"

    #OLD quantization = scale.pixel_length_equator / (1+pixel_distort) 
    quantization = scale.max_pixel_length / (1 + pixel_distort) # max of shapefiles bounds 
    # OLD distort steradians=scale.steradian_per_pixel * (1+pixel_distort)
    steradians=scale.steradian_per_pixel * (1+pixel_distort)**2 # squared area 

    print "converting these shapefiles to one topojson:  ", input_filenames
    step1start=datetime.datetime.now()

    if type(input_filenames)!=type([]):#not  a list of files
        cmd = "node --nouse-idle-notification --max_old_space_size=8192 {topojsoncmd} -s {steradians} -q {quantization} {input_filenames} -o {output_filename}".format(
            topojsoncmd=TOPOJSON,
            steradians=str(steradians),
            quantization=str(quantization),
            output_filename=output_filename,
            input_filenames=input_filenames
            )
    else:
        cmd = "node --nouse-idle-notification --max_old_space_size=8192 {topojsoncmd} -s {steradians} -q {quantization} {input_filenames} -o {output_filename}".format(
            topojsoncmd=TOPOJSON,
            steradians=str(steradians),
            quantization=str(quantization),
            output_filename=output_filename,
            input_filenames=" ".join(input_filenames)
            )

    print "** topojson command: ** ", cmd

    try:
        args = shlex.split(cmd)
        p = subprocess.Popen(args)
    except OSError as e:
       print "***********************************"
       print "**** Install nodejs and topojson.js, see here: https://github.com/mbostock/topojson/wiki/Installation"
       print "**** Edit TOPOJSON='/your_path_bin/topojson"
       print "***********************************"
       print e
       return False
       sys.exit()

    #x=shapefiles2simplifiedtopojson(filenames,steradians,quantization,topojsonfile)
    print "creating.... ", output_filename

    p.wait()
    step1=datetime.datetime.now()-step1start
    print "DONE.... ", output_filename, step1.seconds, "seconds"
    print "1 of 2. Created ", output_filename, step1.seconds, "seconds"

    #print "step 2 of 2: one simplified topojson back to many shapefiles"
    #topojson2shapefiles(input_filenames, output_filename)
    #allsteps=datetime.datetime.now()-step1start
    #print "step 2 and 2 time: ", allsteps.seconds, "seconds"
    #print "---------------------------------------"

def validate_mapscale():
    for z in range(0,17):
        mapscale=MapScale(z)
        print mapscale

if __name__ == "__main__":
    import config
    SHAPEFILE_TEMPLATE = "/vol/tl_2010_{statecode}_tabblock10.shp" #2digit STATE FIPS
    x=config.STATE_FIPS
    print config.STATE_FIPS
    x.remove("48") # TX
    x.remove("06") # CA
    # last 10 jsons to shp
    x=["01","02","04","05","19","20","25","39","40","50"]

    print x
    print len(x)
    for statecode in x[0:2]:
        step1start=datetime.datetime.now()
        print statecode
        fname=SHAPEFILE_TEMPLATE.format(statecode=statecode)
        print fname
        JSON = fname+'.json'
        print JSON
        #shp2topojson(fname, output_filename=OUTPUT_TOPOJSON, zoom=14)
        SHP=[fname]
        topojson2shapefiles(SHP, JSON)
        step1=datetime.datetime.now()-step1start
        print "DONE.... ", JSON, step1.seconds, "seconds"
    """
    # Experiments with Conneticut's shapefile simplification # 
    # Experiments with DC  24 shapefile simplification # 
    fname=SHAPEFILE_TEMPLATE.format(statecode="24")
    OUTPUT_TOPOJSON = fname+'.json'
    print OUTPUT_TOPOJSON
    print fname
    shp2topojson(fname, output_filename=OUTPUT_TOPOJSON, zoom=16)
    JSON="/vol/tl_2010_24_tabblock10.shp.json"
    SHP=["/vol/tl_2010_24_tabblock10.shp"]
    topojson2shapefiles(SHP, JSON)
    """


    #filenames = ["/vol/states/tl_2012_us_state.shp"] ## tested passed
    #filenames = ["/vol/blocks.shp"]
    #OUTPUT_TOPOJSON = '/vol/temp_topo.json'
    #shp2topojson(filenames, output_filename=OUTPUT_TOPOJSON, zoom=16)
    #topojson2shapefiles(filenames, OUTPUT_TOPOJSON)

    #shp2topojson(input_filenames,zoom=16,pixel_distort=25,output_filename=TEMP_FILE)
    
    # zoom 16 distort 25 pixels 1.5M --> 35K
    # zoom 12 distort 0 1.5M --> 46K **
    # zoom 11 distort 0 1.5M --> 25K **

    # Notes: 
    # quantization is needed for proper simplification
    # quantization spreads points out 
    # simplification removes jaggedy areas
    # Bostock provides error from quantization, 
    # we can approx simplification error
