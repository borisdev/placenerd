import time 
import os
import sys
ENV = os.environ['ENV']

if ENV == "DEVELOPMENT":
    while True:
        time.sleep(100)
else:
    print("Missing ENV environment variable?")
    sys.exit()
