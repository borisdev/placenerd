import numpy
from numpy import copy, random, arange
import time

# SETUP    
N=10**5
ids = arange(0,N).astype(str)
values = arange(0,N)
numpy.random.shuffle(ids)
numpy.random.shuffle(values)
ordered_ids=arange(0,N).astype(str)



ordered_valuesA = numpy.empty((N,1))
ordered_valuesA[:] = numpy.NAN
# METHOD 1
start = time.clock()
for i in range(len(values)):ordered_valuesA[ordered_ids==ids[i]]=values[i]
print "not using dictionary:", time.clock() - start

ordered_valuesB = numpy.empty((N,1))
ordered_valuesB[:] = numpy.NAN
# METHOD 2
start = time.clock()
d = dict(zip(ids, values))
for k, v in d.iteritems(): ordered_valuesB[ordered_ids==k] = v
print "using dictionary:", time.clock() - start

ordered_valuesC = numpy.empty((N,1))
ordered_valuesC[:] = numpy.NAN
# METHOD 3
start = time.clock()
dd = dict(zip(ids, values))
ordered_valuesC = [dd.get(m, 0) for m in ordered_ids]
ordered_valuesC = numpy.array(ordered_valuesC)
print "using dictionary with list comprehension:", time.clock() - start

ordered_valuesD = numpy.empty((N,1))
ordered_valuesD[:] = numpy.NAN
# METHOD 4
INDEX = {key:i for i,key in enumerate(ordered_ids)}
start = time.clock()
for k,v in zip(ids, values):
    ordered_valuesD[INDEX.get(k)] = v
print "using dictionary with list comprehension:", time.clock() - start

print "A==B", (ordered_valuesA == ordered_valuesB).all()
print "A==C", (ordered_valuesA == ordered_valuesC).all()
print "A==D", (ordered_valuesA == ordered_valuesD).all()
