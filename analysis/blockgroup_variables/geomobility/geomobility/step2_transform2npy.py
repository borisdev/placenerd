import csv
import sys
import numpy
import tables
from numpy import *
from scipy import stats
import numpy.ma as ma
from scipy.stats import norm
sys.path.append("../")
from order_array import order_array

def simple_stats(myarray,name=""):
    idx=where(isnan(myarray)==False)[0]
    print "mean "+name, mean(myarray[idx])
    print "median "+name, median(myarray[idx])
    print "min "+name, min(myarray[idx])
    print "max "+name, max(myarray[idx])
    print "count "+name, len(myarray[idx])


# TypeError: invalid type (<type 'str'>) for column ``total_mobility_pop``

if __name__ == '__main__':
    #"total_mobility_pop":"JMLE001"
    #"same_house_last_year":"JMLE002"
    #"diff_usamsa_last_year":"JMLE007"
    #"abroad_last_year":"JMLE012"

    #table="../../data/pytables/transpo_mode.h5"
    table="mobility.h5"
    print "loading data..."
    f=tables.open_file(table)
    print "pyTable Fields Description: ", f.root.mygroup.readout

    shpidx=f.root.mygroup.readout.cols.shpidx[:] # TODO: sort before saving .hd5 
    total=f.root.mygroup.readout.cols.total_mobility_pop[:] 
    msa=f.root.mygroup.readout.cols.diff_usamsa_last_year[:] 
    abroad=f.root.mygroup.readout.cols.abroad_last_year[:] 
    geoids=f.root.mygroup.readout.cols.geoid[:] 

    # array needs to be a float to use nan
    # TODO: use nan before saving .hd5
    total = total.astype(numpy.float)
    msa = msa.astype(numpy.float)
    abroad = abroad.astype(numpy.float)
    
    # handles zeros division
    invalidtractidx=where(total==0)[0] # the indexes of tracts with zero population
    validtractidx=where(total!=0)[0] # the indexes of tracts with zero population
    total[invalidtractidx] = numpy.nan # replace 0 with null values, so no division by zero


    percent = msa/total # percent living in different MSA over last year
    percent_z=stats.zscore(ma.masked_invalid(percent)).base
    normcdf=norm.cdf(ma.masked_invalid(percent_z))
    o=order_array(geoids,percent)
    save("mobility_msa_percent",o)

    percent = abroad/total # percent living in different country over last year
    percent_z=stats.zscore(ma.masked_invalid(percent)).base
    normcdf=norm.cdf(ma.masked_invalid(percent_z))
    o=order_array(geoids,percent)
    save("mobility_abroad_percent",o)
