#TODO
# simplify api calls above
# simple metadata above
# compute twiiter scores
# pretty table for validation
# some tests
# make OO

import pysal
#from prettytable import *
import numpy
import numpy as np
import os
import time 
from numpy import *
from time import *
#import redis
import time

# This meta data gets sent to the browser as variables user can choose from
VARS = [ ## This metadata should come from numpy titles in VARIABLES
    {"id":"mixrace", "name":"Racial Mixing", "description":"Percent households that contain members of different races", "weight": 0},
    {"id":"bikers", "name":"Biking", "description":"Ratio of biker riders going to work to car drivers going to work alone", "weight": 0},
    {"id":"walkers", "name":"Walking", "description":"Ratio of walkers going to work to car drivers going to work alone", "weight": 0},
    {"id":"mobility_msa", "name":"Geographic Mobility", "description":"Percent out of MSA in last year", "weight": 0},
    {"id":"mobility_abroad", "name":"Geographic Mobility", "description":"Percent abroad", "weight": 0},
    {"id":"masters_degree", "name":"Highly Educated Females", "description":"Percent Master, Professional, or Doctorate", "weight": 0},
    {"id":"self_employed", "name":"Self-employed", "description":"non-farm", "weight": 0}
]

VARIDX = {var['id']:i for i,var in enumerate(VARS)}

DATA_FILE = os.path.join(os.path.split(__file__)[0], 'variables_percentiles.npy')  
D = numpy.load(DATA_FILE)
DATA=numpy.column_stack((D['mixrace'],D['mobility_abroad'],D["mobility_msa"],D["walkers"],D["bikers"],D["masters_degree"],D["self_employed"]))

VAR_FILE = os.path.join(os.path.split(__file__)[0], 'variables_raw.npy')
VARIABLES = numpy.load(VAR_FILE)

# Areas that had some missing census raw values now have nans and will be made TRANSPERANT
NANS_FILE = os.path.join(os.path.split(__file__)[0], "offsets_with_nans.npy")
IDX_NANS=numpy.load(NANS_FILE)

# Fun Fact: float('nan') != float('nan')
nan2none = lambda x: x if x==x else None

def getVars(offset):
    """user clicks map then popup window
       then angular places api 
       then mygeoscore api.py calls this function 
       to get raw values info about a census block group

       TODO: also return the raw and percentile, and twitter values
    """
    rec = VARIABLES[offset]
    return dict(zip(rec.dtype.names, map(nan2none, rec.tolist())))

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
    percentiles = percentiles+50
    return percentiles

def compute_score(user_weights):
    # just grab the non-zero weights
    valid_weights = {key: value for key, value in user_weights.items() if value is not  0}
    assert len(valid_weights) > 0, "No valid non-zero weights provided" 
    user_vars = valid_weights.keys()
    user_values = [i for i in valid_weights.values()]
    user_values_vector = array(user_values)
    # convert chosen variable columns of structured record array to smaller normal array for matrix alegbra
    matrix=array([D[n] for n in user_vars],dtype=float).T
    #print matrix
    #print user_values_vector
    #print user_vars
    raw_score=matrix.dot(user_values_vector)
    final_scores= percentiles(raw_score)
    round_scores=numpy.around(final_scores) 
    round_scores[IDX_NANS]=numpy.nan # transperant areas
    return round_scores


if __name__ == '__main__':
    ## INPUT user_weights
    user_weights = {
            'bikers':-10, 
            'walkers':0, 
            'masters_degree':3,
            'self_employed':4, 
            'mixrace':5, 
            'mobility_abroad':6,
            'mobility_msa':7
        }
    score = compute_score(user_weights)
    print(score)
