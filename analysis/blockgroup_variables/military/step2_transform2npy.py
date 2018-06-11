import csv
import numpy as nu
import tables
from numpy import *
from scipy import stats
import numpy.ma as ma
from scipy.stats import norm
import sys
sys.path.append("../")
from order_array import order_array
import transform
from transform import getArray
from transform import divideArray



if __name__ == '__main__':
    variable=getArray("military.h5","total_military")
    total=getArray("../age/age.h5","total")
    nu.save("military_percent",divideArray(variable,total))
