import os
import sys
sys.path.append(os.path.abspath('../etl/blockgroup_variables'))
import variables2score as var

weights = {}  # {name: value,...} value is between -4 and 4 
score = var.compute_score(weights)
