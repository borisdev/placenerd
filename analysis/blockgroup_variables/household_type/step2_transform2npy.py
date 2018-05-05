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
    transform.h5_variable2percent("household_type.h5","married")
    transform.h5_variable2percent("household_type.h5","single_dad")
    transform.h5_variable2percent("household_type.h5","single_mom")
    transform.h5_variable2percent("household_type.h5","living_alone")
