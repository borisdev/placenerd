#TODO
# pretty table for validation
# some tests

import numpy as nu
import os
import cPickle as pickle
import transform
import time

percentiles=transform.percentiles

# cbsa 1800+ metro and micro politan areas, cbsa2stcounty.csv source: http://www.census.gov/population/metro/data/def.html
cbsa_file = "cbsa2blockgrp_offsets.pkl"
with open(cbsa_file, 'rb') as fp:
      msa2offsets = pickle.load(fp)

percentiles = nu.load('variables_percentiles.npy')
raw = nu.load('variables_raw.npy')
idx_nans=nu.load("transparent_offsets.npy")

# Areas with zero or missing census population raw values will be made TRANSPERANT
descriptions = {
     "sentiment_overall": { "name":"sentiment","description":"sentiment"}
    ,"mixrace": { "name":"Mixed race","description":"Percent of residents of two or more different races"}
    ,"bikers":{ "name":"Biker commuting","description":"High ratio of bikers compared to drivers who commute to work"}
    ,"walkers":{ "name":"Walk commuting","description":"High ratio of walkers compared to drivers who commute to work"}
    ,"mobility_msa":{ "name":"Just arrived","description":"High percent of residents arrived from a different metro within the year"}
    ,"mobility_abroad":{ "name":"International","description":"High percent of residents lived in another country within the year"}
    ,"masters_degree": { "name":"Highly educated Females", "description": "High percent of women with a masters degree or higher"}
    ,"self_employed":{ "name":"Self-employed", "description":"High percent self-employed, outside of farming"}
    ,"vacant":{"name":"Vacancy", "description":"High percent of housing vacant"}
    ,"twenties":{"name":"Age 20's", "description":"High percent in their twenties"}
    ,"thirties":{"name":"Age 30's", "description":"High percent in their thirties"}
    ,"forties":{"name":"Age 40's", "description":"High percent in their forties"}
    ,"fifties":{"name":"Age 50's", "description":"High percent in their fifties"}
    ,"sixties":{"name":"Age 60's", "description":"High percent in their sixties"}
    ,"seventies":{"name":"Age 70's", "description":"High percent in their seventies"}
    ,"eighties_plus":{"name":"Age 80's", "description":"High percent in their eighties and plus"}
    ,"military":{"name":"Veterans", "description":"High percent of residents are U.S.A military veterans"}
    ,"income":{"name":"High income", "description":"High per capita income"}
    ,"forsale":{"name":"For sale", "description":"High percent housing for sale"}
    ,"married":{"name":"Married", "description":"High percent are married couples"}
    ,"single_mom":{"name":"Single moms", "description":"High percent of single mom households"}
    ,"single_dad":{"name":"Single dads", "description":"High percent of single dad households"}
    ,"living_alone":{"name":"Living alone", "description":"High percent living alone"}
    ,"Under_60min":{"name":"Short commutes", "description":"High percent commute less than 1 hour to work"}
    ,"poverty": {"name":"High poverty", "description":"High percent in poverty"}
    }

def percentiles_msa():
    # not be transformed to percentiles and thats why we get -50s
    final_scores=nu.empty(len(self.raw_score)) 
    # So then....Solution is next line
    final_scores[:]=nu.NAN
    for msa, offsets in msa2offsets.iteritems():
        final_scores[offsets]= percentiles(self.raw_score[offsets])
    round_scores=nu.around(final_scores) 
    round_scores[IDX_NANS]=nu.nan # transperant areas
    return round_scores


print "attributes:", percentiles.dtype.names
print ""
print "Neighborhood Lifstyles: Find significant attributes for each block"
print "-----------------------------------------"
print "-----------------------------------------"

fields=percentiles.dtype.names[1:]
for i in range(len(percentiles)):
    values=nu.array(list(percentiles[i])[1:])+50
    raw_values=nu.array(list(raw[i])[1:])
    print i, "-----------------------------------------"
    for j in range(len(fields)):
        value=values[i]
        if value > 90:
            print descriptions[fields[j]]["name"], "Top", 100-int(values[i]),"percent", raw_values[j+3]
        if value <10 and value >0: # 0 mean null
            print descriptions[fields[j]]["name"], "Bottom", int(values[i]),"percent", raw_values[j+3]
    if i > 10: break

if __name__ == '__main__':
    pass
