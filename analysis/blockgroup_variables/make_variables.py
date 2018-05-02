from numpy import *
from simplejson import *
import pysal
import simplejson
import numpy
import numpy as np
from scipy import stats
import pylab as plt
from prettytable import *

shapefiledbf = '/Users/slow/workspace/choropleth-maps/data/shapefiles/USA_blck_grp/US_blck_grp_2010.dbf'
dbf = pysal.open(shapefiledbf)
shpgeoids = dbf.by_col('GEOID10')
N=len(shpgeoids)
print shapefiledbf
print "count: ", N

shpgeoids=array(shpgeoids)

fieldnames =   [ 'geoids', 'mixrace' ,'mobility_abroad','mobility_msa','walkers', 'bikers', 'masters_degree', 'self_employed']
fieldformats = [ 'a20','f2','f2','f2','f2','f2','f2','f2']

Nvars=len(fieldnames)-1

## TODO: there should be an API that hydrates our catalog, addVariable(array)
mixrace=numpy.load(open("mixrace/mixrace.npy","r"))
mobility_abroad=numpy.load(open("geomobility/mobility_abroad_percent.npy","r"))
mobility_msa=numpy.load(open("geomobility/mobility_msa_percent.npy","r"))
walkers=numpy.load(open("transp_school_selfemp/walker_driver_just_ratio.npy","r"))
bikers=numpy.load(open("transp_school_selfemp/biker_driver_just_ratio.npy","r"))
masters_degree=numpy.load(open("transp_school_selfemp/masters_degree_percent.npy","r"))
self_employed=numpy.load(open("transp_school_selfemp/self_employed_percent.npy","r"))

R = np.zeros(N, dtype={'names': fieldnames ,'formats': fieldformats} )
P = np.zeros(N, dtype={'names': fieldnames ,'formats': fieldformats} )

def percentiles(values):
    """
    nan means there was no data available for that area
    """
    N=len(values)
    middle=median(values)
    new_values=numpy.empty(N)
    ## START handle nans first, makes them median, so they are neutral
    ## and next percentiles argsort() works
    new_values[numpy.where(numpy.isnan(values)==True)[0]]=middle
    ## END handle nans first, makes them median, so they are neutral

    for rank,idx in enumerate(values.argsort()): new_values[idx]=rank + 1 # highest will be big, len(values)
    # new_values ranges now from 1 to very tiny
    #import ipdb; ipdb.set_trace()
    percentiles = (100.0*new_values / N )-50 # range now from 50 to almost -50
    percentiles[numpy.where(numpy.isnan(values)==True)[0]]=0 # force all nans to 0
    percentiles[numpy.where(values==0)[0]]=-50 # force all 0 to -50
    return percentiles

M=numpy.zeros((N,len(fieldnames)-1))
M[:,0]=mixrace
M[:,1]=mobility_abroad
M[:,2]=mobility_msa
M[:,3]=walkers
M[:,4]=bikers
M[:,5]=masters_degree
M[:,6]=self_employed

offsets_with_nans=where(isnan(M.sum(axis=1))==True)[0]
print len(offsets_with_nans), "areas with some  missing values"
print len(where(sum(isnan(M),axis=1)==Nvars)[0]), "areas with all missing values"

R["geoids"]=shpgeoids
R["mixrace"]=mixrace
R["mobility_abroad"]=mobility_abroad
R["mobility_msa"]=mobility_msa
R["walkers"]=walkers
R["bikers"]=bikers
R["masters_degree"]=masters_degree
R["self_employed"]=self_employed

P["geoids"]=shpgeoids
P["mixrace"]=percentiles(mixrace) 
P["mobility_abroad"]=percentiles(mobility_abroad)
P["mobility_msa"]=percentiles(mobility_msa)
P["walkers"]=percentiles(walkers)
P["bikers"]=percentiles(bikers)
P["masters_degree"]=percentiles(masters_degree)
P["self_employed"]=percentiles(self_employed)

indexes_of_nans = numpy.where(numpy.isnan(R["mixrace"])==True)
nanvalues_after_percentile = P["mixrace"][indexes_of_nans]
assert (nanvalues_after_percentile==0).all()==True, "missing values must be 0"

save("offsets_with_nans",offsets_with_nans) # areas with missing values will be transperant
save("variables_raw",R)
save("variables_percentiles",P)


#### SANITY CHECK ######

print "some where in San Bernardino county, CA"
print "geoid ", R[0][0]
print ""
print fieldnames[1:]
table_raw=PrettyTable(fieldnames)
print "raw"
a=[round(i,2) for i in list(R[0])[1:]]
b=[round(i,2) for i in list(R[1])[1:]]
a.insert(0,R[0][0])
b.insert(0,R[1][0])
table_raw.add_row(a)
table_raw.add_row(b)
print table_raw
table_percentiles=PrettyTable(fieldnames)
print ""
print "percentiles"
print ""
print "geoid ", R[1][0]
print ""
print fieldnames[1:]
c=[round(i,2) for i in list(P[0])[1:]]
d=[round(i,2) for i in list(P[1])[1:]]
c.insert(0,R[0][0])
d.insert(0,R[1][0])
table_percentiles.add_row(c)
table_percentiles.add_row(d)
print table_percentiles
