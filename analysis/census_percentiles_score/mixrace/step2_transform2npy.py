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



def simple_stats(myarray,name=""):
    idx=where(isnan(myarray)==False)[0]
    print "mean "+name, mean(myarray[idx])
    print "median "+name, median(myarray[idx])
    print "min "+name, min(myarray[idx])
    print "max "+name, max(myarray[idx])
    print "count "+name, len(myarray[idx])


# TypeError: invalid type (<type 'str'>) for column ``total_mobility_pop``

if __name__ == '__main__':
    #"total":"JMBE001"
    #"mixrace":"JMBE008" 
    table="mixrace.h5"
    print "loading data..."
    f=tables.open_file(table)
    print "pyTable Fields Description: ", f.root.mygroup.readout

    shpidx=f.root.mygroup.readout.cols.shpidx[:] # TODO: sort before saving .hd5 
    total=f.root.mygroup.readout.cols.total[:] 
    mixrace=f.root.mygroup.readout.cols.mixrace[:] 
    geoids=f.root.mygroup.readout.cols.geoid[:] 

    # array needs to be a float to use nan
    # TODO: use nan before saving .hd5
    total = total.astype(numpy.float)
    mixrace = mixrace.astype(numpy.float)
    
    # handles zeros division
    invalidtractidx=where(total==0)[0] # the indexes of tracts with zero population
    validtractidx=where(total!=0)[0] # the indexes of tracts with zero population
    total[invalidtractidx] = numpy.nan # replace 0 with null values, so no division by zero

    percent=(mixrace/total) # percent living in different MSA over last year

    percent_z=stats.zscore(ma.masked_invalid(percent)).base
    normcdf=norm.cdf(ma.masked_invalid(percent_z))
    o=order_array(geoids,percent)
    save("mixrace_percent",o)
