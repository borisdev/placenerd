from numpy import *
import numpy
import numpy as np
import os,sys

import simplejson as json


if __name__=='__main__':
    _this_dir = "."
    sys.path.append("../../../dynTM/src/pyClient")
else: #relative paths are relative to the main script, so above breaks
    _this_dir = os.path.split(__file__)[0]
    sys.path.append(os.path.join(_this_dir, "../../../dynTM/src/pyClient"))
import DynTM

f=open(os.path.join(_this_dir, "name2csid.json"), 'r')
name2csid = json.load(f)


# PRE-LOADED colorscheme and tileset
tsid="dtmUser:80D72034643364302F8D513531046CDC" # blkgrps
#csid="dtmUser:6ce2692e0d731342946bd75e69b1790d" # purple to orange of count 10
csid='dtmUser:26e9f9fabc6f9293812ffc9946a4aee6' # 18 bins dark green to dark red
csid=name2csid["PurplesOranges"]
csid=name2csid["GreensReds"]

names=name2csid.keys()
Nnames=len(names)

# make a client instance
AccessKeyID = 'dtmUser'
AccessKey = 'key'
border = False
client=DynTM.GeoDaWS_DynTM(AccessKeyID=AccessKeyID,AccessKey=AccessKey)
N=client.describeTileSet(tsid)['numregions']


# main function
def scores2map(scores):
    """
    >>> map_params=scores2map(np.load("variables.npy")["walkers"])
    >>> png = client.getTile(map_params["ts"], 4, 2, 5,map_params["cl"],map_params["cs"], border)

    """
    # Randomly change colorschemes 
    #idx=random.randint(0,Nnames)
    #print "RANDOM INT", idx
    #name=names[idx]
    #print "RANDOM SCHEME", name
    #csid=name2csid[name]

    if scores.shape[0] != N:
        raise ValueError, "Error: must have same scores as blkgrps : %r" % N
    scores.shape = (N,) ## this no works  scores.shape == (N,1):

    ### PERCENTILE SCORES TO CLASSLIST ###
    # input scores have been standarized to be integers ranging from 0 to 100
    scores = scores + 2 # 0 and 1 are reserved for background and border
    scores[np.isnan(scores)]=0# missing value areas are transperant areas
    classlist=list(scores.astype(int)) # rounds to floor 

    ## Data validation should be on client side?
    #unique_classes=np.unique(scores)
    #print "unique scores: ", unique_classes, "should be 0, no 1 reserverd for border  2,3,...101"
    #Nc=len(unique_classes)
    #print "length unique scores: ", Nc, "should be 101"
    #Ns=len(scores)
    # 100 colors plus transperant color means 101 classes
    #assert Nc <= 102, "Error: must have unique classes =< 101 colorscheme: %r" % Nc
    #assert Ns==N, "Error: classification array must be blkgrp count: %r" % len(Ns)

    classification_id = client.createClassification(tsid, classlist)
    return {"cl":classification_id,"cs":csid,"ts":tsid} 


if __name__ == '__main__':
    # tile coordinates to display USA's northwest
    map_params=scores2map(np.load("variables.npy")["bikers"])
    png = client.getTile(map_params["ts"], 4, 2, 5,map_params["cl"],map_params["cs"], border)
