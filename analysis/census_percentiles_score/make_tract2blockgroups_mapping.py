import pysal
import numpy
from numpy import *

"""
The output of this module is used to interpolate blockgroup values using 
aggreagte tract values.

The output is saved as a pickle file of a python dictionary.

The dictionary mapping of one tract to its many blockgroup members and  appears as below.

    .
    .
    .
    '72151950900': array([80211, 81086, 82658]),
    '72151951000': array([74282, 83454]),
    '72151951100': array([80212, 80213]),
    '72151951200': array([75031, 83068, 86181]),
    '72151951300': array([74271, 75461, 86189]),
    '72153750101': array([75317, 81406]),
    '72153750102': array([80464, 80865]),
    .
    .
    .
"""
# SHAPEFILE'S GEOIDS
try:
    shapefiledbf = '/Users/slow/workspace/choropleth-maps/data/shapefiles/USA_blck_grp/US_blck_grp_2010.dbf'
    dbf = pysal.open(shapefiledbf)
    shpgeoids_list = dbf.by_col('GEOID10')
except:
    shapefileNP = os.path.join(os.path.split(__file__)[0], "variables_percentiles.npy")
    shpgeoids_list = numpy.load(shapefileNP)['geoids'].tolist()
N=len(shpgeoids_list)
print shapefiledbf
print "count: ", N
tractsids= array([ geoid[:-1] for geoid in shpgeoids_list ])
tractkey2blockidxs={}
for key in unique(tractsids):
    tractkey2blockidxs[key]=where(tractsids==key)[0]

import cPickle as pickle
with open("tractkey2blockidxs.pkl", 'wb') as fp:
      pickle.dump(tractkey2blockidxs, fp)

