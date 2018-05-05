import csv
import numpy
import tables
from numpy import *
from scipy import stats
import numpy.ma as ma
from scipy.stats import norm
import sys
sys.path.append("../")
from order_array import order_array
import transform




if __name__ == '__main__':
    transform.h5_variable2array("nested_geo_with_pop.h5","total")
    transform.h5_variable2stringArray("nested_geo_with_pop.h5","stateName")
    transform.h5_variable2stringArray("nested_geo_with_pop.h5","stateCode")
    transform.h5_variable2stringArray("nested_geo_with_pop.h5","countyName")
    transform.h5_variable2stringArray("nested_geo_with_pop.h5","countyCode")
    transform.h5_variable2stringArray("nested_geo_with_pop.h5","placeName")
    transform.h5_variable2stringArray("nested_geo_with_pop.h5","placeCode")
    transform.h5_variable2stringArray("nested_geo_with_pop.h5","msaName")
    transform.h5_variable2stringArray("nested_geo_with_pop.h5","msaCode")
