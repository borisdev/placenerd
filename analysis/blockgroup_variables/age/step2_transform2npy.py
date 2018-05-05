import csv
import numpy
import tables
import numpy as nu
from scipy import stats
import numpy.ma as ma
from scipy.stats import norm
import sys
sys.path.append("../")
from order_array import order_array
from transform import getArray
import transform
from transform import lq

#def getArray(file_name,variable_name):
#def lq(total,arrayvariable,arrayvariable_name):

if __name__ == '__main__':
    ages={
             "twenties"      :["20","21","22to24","25to29"]
            ,"thirties"      :["30to34","35to39"]
            ,"forties"       :["40to44","45to49"]
            ,"fifties"       :["50to54","55to59"]
            ,"sixties"       :["60and61","62to64","65and66", "67to69"]
            ,"seventies"     :["70to74","75to79"]
            ,"eighties_plus" :["80to84","85over"]
        }
    total=getArray("age.h5","total")
    for age_group in ages.keys():
        for i,v in enumerate(ages[age_group]):
            # male + female
            if i == 0:
                variable=getArray("age.h5","Male"+v) + getArray("age.h5","Female"+v)
            else:
                variable=variable + getArray("age.h5","Male"+v) + getArray("age.h5","Female"+v)
        percent=variable/total
        nu.save(age_group+"_percent",percent)
