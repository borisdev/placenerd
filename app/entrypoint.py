import time 
import logging
import os
import sys
ENV = os.environ['ENV']
logging.info(ENV)

if ENV == "DEV":
    while True:
        time.sleep(100)
else:
    print("Missing ENV environment variable?")
    sys.exit()
