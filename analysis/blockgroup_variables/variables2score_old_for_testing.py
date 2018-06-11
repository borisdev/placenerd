import pysal
from prettytable import *
import numpy
import numpy as np
import os
import time 
from numpy import *
from time import *
import redis
import time

# This meta data get sent to the browses
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
VAR_FILE = os.path.join(os.path.split(__file__)[0], 'variables_raw.npy')
D = numpy.load(DATA_FILE)
DATA=numpy.column_stack((D['mixrace'],D['mobility_abroad'],D["mobility_msa"],D["walkers"],D["bikers"],D["masters_degree"],D["self_employed"]))

## DATA_ORDER:
#['mixrace',
#'mobility_abroad',
#'mobility_msa',
#'walkers',
#'bikers',
#'masters_degree',
#'self_employed']

## Areas with all nan NEED TO BE TRANSPERANT
NANS_FILE = os.path.join(os.path.split(__file__)[0], "offsets_with_nans.npy")
IDX_NANS=numpy.load(NANS_FILE)

# make sure there are no +inf, -inf

VARIABLES = numpy.load(VAR_FILE)
DATA_ORDER=list(VARIABLES.dtype.names[1:])

# Fun Fact: float('nan') != float('nan')
nan2none = lambda x: x if x==x else None

def getVars(offset):
    """mygeoscore api.py calls this function, after places api asks for info about
    a census block group

    TODO: also return the raw and percentile, and twitter values
    """
    rec = VARIABLES[offset]
    return dict(zip(rec.dtype.names, map(nan2none, rec.tolist())))

def user_weights2vector(user_weights, DATA_ORDER=DATA_ORDER):
    N=len(DATA_ORDER)
    w=numpy.zeros((N,1))
    count_valid_weights=0
    # reorder weights and validate weights before compute
    for k, v in user_weights.iteritems(): 
        try:
            w[DATA_ORDER.index(k)]=v # order the values
            if user_weights[k]!=0:
                count_valid_weights+=1
        except ValueError as e:
            raise ValueError, "User gave a variable name not in the geoscore catalog: " + repr(e)
    assert count_valid_weights > 0, "No valid non-zero weights provided" 
    return w.reshape(N,)

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


def compute_score_normal(user_weights, DATA=DATA, DATA_ORDER=DATA_ORDER):
    if hasattr(DATA, '__call__'):
        DATA=DATA()
    #print user_weights
    w=user_weights2vector(user_weights, DATA_ORDER=DATA_ORDER)
    print DATA
    print w
    raw_score=DATA.dot(w)
    # For some reason below takes much much longer though its scipy and simpler??
    #[int(stats.percentileofscore(scores,x)) for x in raw_score]
    final_scores= percentiles(raw_score)
    round_scores=numpy.around(final_scores) 
    round_scores[IDX_NANS]=numpy.nan # transperant areas
    #print "unique scores: ", numpy.sort(numpy.unique(round_scores))
    return round_scores

def compute_score_twitter(user_weights):
    matrix=get_tweet_data()
    #print user_weights
    w=user_weights2vector(user_weights, DATA_ORDER=DATA_ORDER)
    raw_score=matrix.dot(w)
    # For some reason below takes much much longer though its scipy and simpler??
    #[int(stats.percentileofscore(scores,x)) for x in raw_score]
    final_scores= percentiles(raw_score)
    round_scores=numpy.around(final_scores) 
    # no tweets already set as 0 # round_scores[IDX_NANS]=numpy.nan # transperant areas
    #print "unique scores: ", numpy.sort(numpy.unique(round_scores))
    return round_scores


class Geoscore():

    def __init__(self, weights):
        self.weights=weights

    def load_variable_into_matrix(self):
        pass

    def compute_score(self):

        pass    
        #return scores

def compute_score(user_weights):
    if APP=="TWITTER": 
        return compute_score_twitter(user_weights)
    else:
        return compute_score_normal(user_weights, DATA=DATA, DATA_ORDER=DATA_ORDER)


def compute_scores2(user_weights):
    ## TODO do pretty table validation
    # just grab the non-zero weights
    valid_weights = {key: value for key, value in user_weights.items() if value is not  0}
    assert len(valid_weights) > 0, "No valid non-zero weights provided" 
    user_vars = valid_weights.keys()
    user_values_vector = array(valid_weights.values())
    # convert chosen variable columns of structured record array to smaller normal array for matrix alegbra
    matrix=array([D[n] for n in user_vars],dtype=float).T
    print matrix
    print user_values_vector
    print user_vars
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
    start=time.clock()
    scores=compute_score_normal(user_weights,DATA_ORDER=DATA_ORDER)
    scores2=compute_scores2(user_weights)
    idx=np.where(scores!=scores2)[0] # remember nan != nan
    print "You should see 4x True:"
    print 43081==len(idx)
    print 176693==len(np.where(scores==scores2)[0])
    print isnan(scores[idx]).all()
    print isnan(scores2[idx]).all()

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
    """
    ## Below shows logic of scoring with a small make believe sample

    # TEST NUMBERS
    DATA_ORDER = ['bike','walk','christian']
    TX  = numpy.array([ -40, -50,  50]).reshape(1,3)
    NY  = numpy.array([  50,  50, -50]).reshape(1,3)
    DC  = numpy.array([  40,  40, -20]).reshape(1,3)
    AZ  = numpy.array([   0,   0,   0]).reshape(1,3)
    NJ  = numpy.array([   4,   4,  -2]).reshape(1,3)
    DATA=numpy.vstack((TX,NY,DC,AZ,NJ))
    user_weights={'bike':4,'walk':0,'christian':-4}
    print DATA_ORDER
    print DATA
    print "user_weights", user_weights
    w=user_weights2vector(user_weights,DATA_ORDER)
    print "weights vector"
    print w.T
    raw_score=DATA.dot(w)
    print ""
    #print "TX, NY, DC, AZ, NJ"
    print "raw_score"
    print raw_score.T
    #rankings = (-1*raw_score).argsort(0) +1
    print "rankings"
    #print rankings.T
    #percentiles = 100.0*rankings/len(DATA) # plus 1 so top is 100, not 99 
    print "percentiles"
    p=percentiles(raw_score)
    print p
    assert p[1]==100, "scores is broken"
    """
