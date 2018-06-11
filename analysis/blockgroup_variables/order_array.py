from numpy import *
from simplejson import *
import pysal
import simplejson
import numpy

shapefiledbf = '/Users/slow/workspace/choropleth-maps/data/shapefiles/USA_blck_grp/US_blck_grp_2010.dbf'
dbf = pysal.open(shapefiledbf)
shpgeoids = dbf.by_col('GEOID10')
N=len(shpgeoids)
print shapefiledbf
print "count: ", N

shpgeoids=array(shpgeoids)

import numpy as np

def order_array(ids,values,master_order_ids=shpgeoids):
    """    
    >>> ids=array(["12","2","3"])
    >>> values=array([12,20,30])
    >>> master_order_ids=array(["1","2","3","4","5","6"])
    >>> order_array(ids,values,master_order_ids)
    ordered [  0.  20.  30.   0.   0.   0.]
    """
    assert(len(values)==len(ids))
    ordered_values=zeros(len(master_order_ids))

    for i in range(len(values)):
        ordered_values[where(master_order_ids==ids[i])]=values[i]

    print "ordered", ordered_values
    return ordered_values

if __name__ == '__main__':
    ids=array(["12","2","3"])
    values=array([12,20,30])
    master_order_ids=array(["1","2","3","4","5","6"])
    order_array(ids,values,master_order_ids)

