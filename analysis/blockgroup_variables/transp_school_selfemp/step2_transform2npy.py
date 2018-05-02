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



if __name__ == '__main__':
    #table="../../data/pytables/transpo_mode.h5"
    table="transpo_mobility_schooling.h5"
    print "loading data..."
    f=tables.open_file(table)
    print "pyTable Fields Description: ", f.root.mygroup.readout

    shpidx=f.root.mygroup.readout.cols.shpidx[:] # TODO: sort before saving .hd5 
    total_transpo=f.root.mygroup.readout.cols.total_transpo[:] 
    drove_alone=f.root.mygroup.readout.cols.drove_alone[:] 
    bicycle=f.root.mygroup.readout.cols.bicycle[:] 
    walked=f.root.mygroup.readout.cols.walked[:] 
    total_mobility=f.root.mygroup.readout.cols.total_mobility[:] 
    diffMSA_mobility=f.root.mygroup.readout.cols.diffMSA_mobility[:] 
    total_schooling=f.root.mygroup.readout.cols.total_schooling[:] 
    MA_schooling=f.root.mygroup.readout.cols.MA_schooling[:] 
    walked=f.root.mygroup.readout.cols.walked[:] 
    selfemp_total=f.root.mygroup.readout.cols.selfemp_total[:] 
    selfemp=f.root.mygroup.readout.cols.selfemp[:] 
    geoids=f.root.mygroup.readout.cols.geoid[:] 

    # array needs to be a float to use nan
    # TODO: use nan before saving .hd5
    bicycle = bicycle.astype(numpy.float)
    walked = walked.astype(numpy.float)
    drove_alone = drove_alone.astype(numpy.float)
    selfemp_total = selfemp_total.astype(numpy.float)
    selfemp = selfemp.astype(numpy.float)
    total_schooling = total_schooling.astype(numpy.float)
    MA_schooling = MA_schooling.astype(numpy.float)
    
    # handles zeros division for bikers and walkers ratios
    invalidtractidx=where(drove_alone==0)[0] # the indexes of tracts with zero population
    drove_alone[invalidtractidx] = numpy.nan # replace 0 with null values, so no division by zero

    percent = (bicycle / drove_alone) 
    #percent_z=stats.zscore(ma.masked_invalid(percent)).base
    #normcdf=norm.cdf(ma.masked_invalid(percent_z))
    o=order_array(geoids,percent)
    save("biker_driver_just_ratio",o)

    percent = (walked / drove_alone)
    #percent_z=stats.zscore(ma.masked_invalid(percent)).base
    #normcdf=norm.cdf(ma.masked_invalid(percent_z))
    o=order_array(geoids,percent)
    save("walker_driver_just_ratio",o)

    # handles zeros division for self_employed percentiles
    invalidtractidx=where(selfemp_total==0)[0] # the indexes of tracts with zero population
    selfemp_total[invalidtractidx] = numpy.nan # replace 0 with null values, so no division by zero

    percent= (selfemp/selfemp_total)
    #percent_z=stats.zscore(ma.masked_invalid(percent)).base
    #normcdf=norm.cdf(ma.masked_invalid(percent_z))
    o=order_array(geoids,percent)
    save("self_employed_percent",o)

    # handles zeros division for masters degrees
    invalidtractidx=where(total_schooling==0)[0] # the indexes of tracts with zero population
    validtractidx=where(total_schooling!=0)[0] # the indexes of tracts with zero population
    total_schooling[invalidtractidx] = numpy.nan # replace 0 with null values, so no division by zero

    percent = (MA_schooling/total_schooling) # percent living in different country over last year
    #percent_z=stats.zscore(ma.masked_invalid(percent)).base
    #normcdf=norm.cdf(ma.masked_invalid(percent_z))
    o=order_array(geoids,percent)
    save("masters_degree_percent",o)


    #x=vstack((biking,walking,selfworking,schooling))
    #D=x.T # N rows by 4 attribute columns: biking,walking,selfworking,schooling
    #save("bikers_walkers_selfemployed_mastersdegrees",D)
