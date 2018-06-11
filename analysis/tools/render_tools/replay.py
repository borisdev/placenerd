#! /usr/bin/env python
import math
import csv
import requests
import gevent
import grequests
import time
import sys
import random
import numpy
import datetime
import os
from os import path
from optparse import OptionParser, OptionValueError
import getpass
import subprocess
import re

"""
<<<<<<< HEAD
                Usage Examples                          Approx. duration
                ===========================             ===============
                $python replay.py mapfluence elections     
                $python replay.py geoscore ca-blocks     
                $python replay.py geoscore usa-blocks     
                $python replay.py -x=random -n 2 QA23 tornados 

                Randomization happen between these points:

                    - Seattle latitude 47.610241 longitude -122.334698
                    - Miami latitude 25.77 longitude -80.203  
=======
Usage:

$python replay.py <host> <request_type>

                Usage Examples                                        Approx. duration
                ===========================                           ===============
                $python replay.py <ip_address_host> usatracts   
                $python replay.py <ip_address_host> cablocks     
                $python replay.py localhost cablocks     
                $python replay.py geoscore cablocks     
                $python replay.py geoscore usatracts     

>>>>>>> 055823c53b81223b6ebe1cf0dfab11daef3ee042
"""

# Tests default to the center of the US
DEFAULT_CENTER = (39.0, -96.0)

parser = OptionParser(usage="""
replay.py [options] <target_server> <request_pool>

replay a request pool file against the specified server
""")

def int_list(option, opt, value, parser):
    try:
        setattr(parser.values, option.dest, [int(v) for v in value.split(',')])
    except ValueError:
        raise OptionValueError("zooms list must be a list of ints")

def center_arg(option, opt, value, parser):
    if value == 'random':
        setattr(parser.values, option.dest, 'random')
        return

    try:
        [lat, lon] = [float(v) for v in value.split(',')]
        setattr(parser.values, option.dest, (lat, lon))
    except ValueError:
        raise OptionValueError("center must be lat,lon or 'random'")

def opacity_arg(option, opt, value, parser):
    if value == 'random':
        setattr(parser.values, option.dest, 'random')
        return
    try:
        v = float(value)
        setattr(parser.values, option.dest, v)
    except ValueError:
        raise OptionValueError("opacity must be a float or 'random'")

def api_key_arg(option, opt, value, parser):
    if not value:
        value = 'UMIKEY'
    elif value == 'none':
        value = None
    setattr(parser.values, option.dest, value)

parser.add_option("-r", "--remote", dest="remote",
                  help="run replay script on a remote machine.")
parser.add_option("-p", "--push", dest="push", action="store_true",
                  help="""push replay resources to remote machine.  When -r is
                          not specified, this option is ignored.""")
parser.add_option("-c", "--clear-cache", dest="cache",
                  help="clear the specified cache machine before running tests.")
parser.add_option("-z", "--zoom-levels", dest="zooms", default=[10,11,12,13,14],
                  action='callback', type='string', callback=int_list,
                  help="""comma-separated list of zoom levels to test at.  Not
                          all tests use this feature.""")
parser.add_option("-x", "--center", dest="center", default=DEFAULT_CENTER,
                  action='callback', type='string', callback=center_arg,
                  help="""lat,long of center of test.  Defaults to center of
                          US.  For random center, set it to 'random'.""")
parser.add_option("-n", "--num-rounds", dest="rounds", type="int", default=1,
                  help="number of rounds to run test.  Defaults to 1.")
parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                  help="be verbose")
parser.add_option("-a", "--restart-apache", dest="restart_apache",
                  action="store_true", help="restart apache before testing")
parser.add_option("-k", "--api-key", dest="api_key", default="UMIKEY",
                  action='callback', type='string', callback=api_key_arg,
                  help="""API key to use in queries.  Defaults to 'UMIKEY'.  If
                          you set this to 'none', replay will attempt to use
                          API keys from logfiles.""")
parser.add_option("-o", "--opacity", dest="opacity", default="1.0",
                  action='callback', type='string', callback=opacity_arg,
                  help="""opacity of tile to request.  It can be a float 1.0 or
                          less or the special word 'random'.  Note that this is
                          really only applied as a special case to the election
                          tiles at this time for legacy reasons.  Most tile URIs
                          actually have hard-coded opacity of 0.5""")
parser.add_option("-m", "--max-connections", dest="max_conn", type="int",
<<<<<<< HEAD
                  default=1,
#                  default=49,
=======
                  default=49,
>>>>>>> 055823c53b81223b6ebe1cf0dfab11daef3ee042
                  help="""The max number of concurrent connections allowed.
                          When unspecified, this defaults to 49 so that a
                          7x7-tile map can be loaded concurrently.  For fully
                          synchronous fetches, set this to 1.  For unlimited
                          connections, set to 0.""")
parser.add_option("-f", "--file", dest="file",
                  help="Store response data in a tab file for post-processing.")

(options, args) = parser.parse_args()

if len(args) != 2:
    parser.error("server and request_pool args are required")

RELEASE_SERVER = args[0]
REQUEST_POOL = args[1]

if options.cache:
    try:
        cmd = "sudo redis-cli flushall"
        if options.cache == 'localhost':
            err = subprocess.call(cmd, shell=True)
        else:
            import pxssh, ssh
            print "Connecting to cache machine", options.cache
            user = getpass.getuser()
            conn = ssh.ssh(user, options.cache)
            err = conn.cmd(cmd)
            conn.logout()
        if err:
            print "Failed to clear cache on", options.cache
            sys.exit(err)

    except ImportError:
        print "ERROR: Please pip install pexepct to use remote option"
        sys.exit(1)

    except pxssh.ExceptionPxssh as e:
        print e
        print "Failed to login to", options.cache
        sys.exit(1)

if RELEASE_SERVER == ".": 
    RELEASE_SERVER="localhost"
if RELEASE_SERVER == "QA22": 
    RELEASE_SERVER="ec2-50-17-34-80.compute-1.amazonaws.com"
if RELEASE_SERVER == "CDN": 
    RELEASE_SERVER="dt9pqwl1jfc7x.cloudfront.net"
if RELEASE_SERVER == "mapfluence": 
    RELEASE_SERVER="query.mapfluence.com"
if RELEASE_SERVER == "geoscore": 
    RELEASE_SERVER="api.geoscore.com"


request_pool_dir = os.path.join(os.path.dirname(__file__), "request-pools")
if REQUEST_POOL == "1day": 
    REQUEST_POOL = os.path.join(request_pool_dir, "1day-MF2-status-200May1.csv")
elif REQUEST_POOL == "1500": 
    REQUEST_POOL = os.path.join(request_pool_dir, "1500-tiles.csv")
elif REQUEST_POOL == "100": 
    REQUEST_POOL = os.path.join(request_pool_dir, "100-tiles.csv")
elif REQUEST_POOL == "10": 
    REQUEST_POOL = os.path.join(request_pool_dir, "10-tiles.csv")
elif REQUEST_POOL == "keyauth":
    # This is a special case.  We override the api_key argument to get the
    # legacy behavior.
    options.api_key = None
    import splunksavedsearch 
    splunksavedsearch.main()
    REQUEST_POOL = os.path.join(request_pool_dir, "keyauth.csv")
elif REQUEST_POOL == "catalog":
    REQUEST_POOL = os.path.join(request_pool_dir, "catalog.csv")

if not options.remote:
    print "server", RELEASE_SERVER

if options.remote:
    try:
        import pxssh, ssh
    except ImportError:
        print "ERROR: Please pip install pexepct to use remote option"
        sys.exit(1)
    user = getpass.getuser()
    remote_dir = "/tmp/replay-" + user
    if options.push:
        print "Pushing resources to", options.remote
        # push over the script and the request pool (if it represents a file)
        rp = ""
        if os.path.isfile(REQUEST_POOL):
            rp = REQUEST_POOL
        cmd = "rsync -R %s %s %s:%s/" % \
              (sys.argv[0], rp, options.remote, remote_dir)
        try:
            err = subprocess.call(cmd + " > /dev/null", shell=True)
        except OSError as e:
            print e
            err = -1
        if err:
            print "ERROR: Failed to push resources to " + options.remote
            print "COMMAND: " + cmd
            sys.exit(1)

    try:
        print "Connecting to", options.remote
        opts = sys.argv[:-1]
        for o in ['-r', '--remote', '-c', '--clear-cache']:
            if o in opts:
                i = opts.index(o)
                opts = opts[0:i] + opts[i+2:]
        [opts.remove(o) for o in ['-p', '--push'] if o in opts]
        conn = ssh.ssh(user, options.remote)
        cmd = 'cd ' + remote_dir +'; python ' + ' '.join(opts)
        # Often the request pool has some weirdo chars that bash wants to hang
        # onto (e.g., |, &) so re-quote it.
        cmd += " '" + REQUEST_POOL + "' "
        err = conn.cmd(cmd)

    except pxssh.ExceptionPxssh as e:
        print e
        print "Failed to login to", options.remote
        err = 1

    finally:
        if err:
            print "Failed to remotely execute replay."
        conn.logout()
        sys.exit(err)

if options.restart_apache:
    # Restart apache on the target machine.
    try:
        print "Restarting apache"
        cmd = "sudo apache2ctl restart"
        if RELEASE_SERVER == "localhost":
            err = subprocess.call(cmd, shell=True)
        else:
            import pxssh, ssh
            print "Connecting to target machine", RELEASE_SERVER
            user = getpass.getuser()
            conn = ssh.ssh(user, RELEASE_SERVER)
            err = conn.cmd(cmd)
            conn.logout()
        if err:
            print "ERROR: Failed to restart apache."
            sys.exit(1)

    except ImportError:
        print "ERROR: Please pip install pexepct to use remote option"
        sys.exit(1)

    except pxssh.ExceptionPxssh as e:
        print e
        print "Failed to login to", RELEASE_SERVER
        sys.exit(1)

class Errorpool(object):pass
#TODO: setattr (x, 'name', 'valueZZZ')

class Requestpool(object):

    SINGLE_TILES={"election":"/2.0/UMIKEY/tile/d/opacity={OPACITY}|mode=theme|from=umi.us_census00.county_geometry|date=2009-01-01T08:00:00Z|select=umi.us_elections.2008_pres.prt_dem_pty|breaks=0.2,0.45,0.55,0.8|border=222_0.5|styles=d7191c,fdae61,ffffbf,abd9e9,2c7bb6/g/{z}/{x}/{y}.png"}

#http://api.geoscore.com/dyntm/t?ts=dtmUser:2602F1384BA06F1C6F68E9A6676CDA1A&z=8&x=74&y=99&b=0&cl=dtmUser:db976bf64c8f723c979240837802effa&cs=dtmUser:40aac4a89e31617840589bd4a9bf24b3
#http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=12&x=704&y=1634

    URIS=[  
            ("usatracts","/dyntm/t?ts=dtmUser:2602F1384BA06F1C6F68E9A6676CDA1A&z={z}&x={x}&y={y}&b=0&cl=dtmUser:db976bf64c8f723c979240837802effa&cs=dtmUser:40aac4a89e31617840589bd4a9bf24b3"),
            ("cablocks","/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z={z}&x={x}&y={y}"),
            ("elections","/2.0/UMIKEY/tile/d/opacity=0.5|mode=theme|from=umi.us_census00.county_geometry|date=2009-01-01T08:00:00Z|select=umi.us_elections.2008_pres.prt_dem_pty|breaks=0.2,0.45,0.55,0.8|border=222_0.5|styles=d7191c,fdae61,ffffbf,abd9e9,2c7bb6/g/{z}/{x}/{y}.png"),
         ]
    SURIS=[  

            ("spatialorder","/2.0/{APIKEY}/spatialquery.json?select=id%2Cname%2Carea%2Ccountry%2Cadmin1&from=umi.neighborhoods.geometry&where=intersects%28range%280.01km%2C%7B%22type%22%3A%22Point%22%2C%22coordinates%22%3A%5B{LON}%2C{LAT}%5D%7D%29%29&date=2013-01-15T01%3A35%3A16Z&order_by=area"),
            ("spatialzipcodes","/2.0/{APIKEY}/spatialquery.json?select=name,centroid,admin1&where=intersects(range(3mi,%20{%22type%22:%22Point%22,%22coordinates%22:[{LON},{LAT}]}))&from=umi.us_census00.zcta_geometry&date=2010-02-01T08:00:00Z"),
            ("spatialhoods",'/2.0/{APIKEY}/spatialquery.json?select=name&where=intersects({"type":"Point","coordinates":[{LON},{LAT}]})&from=umi.neighborhoods.geometry')
         ]

    errortypes={}

    def __init__(self, request_pool=REQUEST_POOL, server=RELEASE_SERVER,
                 zooms=["10","11","12","13","14"], center=DEFAULT_CENTER,
                 rounds=1, opacity=1, max_conn=49):
        self.request_name = request_pool
        self.request_pool = request_pool
        self.progress = 0
        self.statusok = 0
        self.statusfail = 0
        self.statuserror = 0
        self.counterrortypes = 0
        self.errorpools = {}
        self.server= "http://" + server
        self.zooms=zooms
        self.zoom = 10 # default zoom 
        self.center = center
        self.rounds=rounds
        self.name2results={}
        self.name2uri=dict(self.URIS)
        self.name2suri=dict(self.SURIS)
        self.opacity = opacity
        self.max_conn = max_conn
        self.TILE_SIZE = 4 # 16 async request block

    def run(self):
        self.start = time.time()
        if options.verbose:
            print "Request Pool:", self.request_pool

        #if self.request_pool == 'election':
        #    print "Server:", self.server 
        #    print "Request Group:", self.request_pool
        #    name="election"
        #    self.request_pool = self.SINGLE_TILES[name]
        #    self.urls = self.buildrequests()
        #    self.singletilerequests(name)
        #    self.summarizeresults(name)

        elif self.request_pool == 'spatial':
            print "Server:", self.server 
            print "Request Group:", self.request_pool
            print "-----------------------------------"
            for name,uri in self.name2suri.items():
                print "Name: ", name
                self.request_pool = self.name2suri[name]
                self.urls = self.buildrequests()
                self.spatialqueries(name)
                self.summarizeresults(name)

        elif self.request_pool in self.name2uri.keys():
            print "making requests for", self.request_pool
            name = self.request_pool
            self.request_pool = self.name2uri[name]
            self.urls = self.buildrequests()
            self.gettileblocks(name)
            self.summarizeblockresults(name)
            print "Reminder: Did you clear the cache? "

        elif self.request_pool == ".":
            for name,uri in self.name2uri.items():
                print "making requests for", name 
                self.request_pool = self.name2uri[name]
                self.urls = self.buildrequests()
                self.gettileblocks(name)
                self.summarizeblockresults(name)
            print "Reminder: Did you clear the cache? "

        else:
            self.urls = self.buildrequests()
            self.asyncrun()
            self.asynclog()
            self.reporterrors()
        self.end = time.time()

    def get_center(self):
        if self.center == 'random':
            usaLatmin=26*10**10
            usaLatmax=48*10**10
            usaLonmin=81*10**10
            usaLonmax=122*10**10
            lat = random.randint(usaLatmin, usaLatmax) / 10**10.0000000000000000
            lon = -1 * random.randint(usaLonmin, usaLonmax) / 10**10.00000000000
            return (float(lat), float(lon))
        else:
            return self.center

    def get_opacity(self):
        if self.opacity == 'random':
            return random.randint(0,100) / 100.0
        else:
            return self.opacity

    def summarizeresults(self,name):
        rs=self.name2results[name] #1st requests slow when initialize connection should be skipped
        values=[name,round(numpy.mean(rs),2), round(numpy.max(rs),2),round(numpy.std(rs),2)]
        print "---summary results-----"
        print "layername,mean,max,std\n"
        print ",".join([str(i) for i in values])
        print "-----------------------"

    def summarizeblockresults(self,layername):
        rs=self.name2results[layername][:,1:] #1st initialization zoom skipped
        values=[layername,round(numpy.mean(rs),2), round(numpy.max(rs),2),round(numpy.std(rs),2)]
        print "---summary results-----"
        print "layername,mean,max,std\n"
        print ",".join([str(i) for i in values])
        print "-----------------------"

    def singletilerequests(self, name):
        self.name2results[name]=[]
        for i,url in enumerate(self.urls):
            start=time.time() # start
<<<<<<< HEAD
            r=requests.head(url)
=======
            r=requests.get(url)
>>>>>>> 055823c53b81223b6ebe1cf0dfab11daef3ee042
            delta=time.time()-start
            self.name2results[name].append(delta)
            T=str(round(delta, 2))
            print "TIME: ",T
            if r.status_code != 200:
                print "Warning: NOT OK"
                print "url: ", url
                print "--------------------------------------------------"
    
    def spatialqueries(self, name):
        self.name2results[name]=[]
        for idx, url in enumerate(self.urls):
            start=time.time() # start
<<<<<<< HEAD
            r=requests.head(url)
=======
            r=requests.get(url)
>>>>>>> 055823c53b81223b6ebe1cf0dfab11daef3ee042
            delta=time.time()-start
            if idx !=0 and delta>5: break
            self.name2results[name].append(delta)
            #print "time: ",delta 
            #print "url: ",url 
            #print "--------------------------------------------------"
            if r.status_code != 200:
                print "Warning: NOT OK"
                print "url: ", url
                print "--------------------------------------------------"

    def gettileblocks(self, layername):
        self.name2results[layername]=numpy.zeros([self.rounds, int(len(self.zooms))])
<<<<<<< HEAD
        TEST=[
        "http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=175&y=408"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=175&y=409"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=175&y=410"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=175&y=411"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=176&y=408"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=176&y=409"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=176&y=410"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=176&y=411"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=177&y=408"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=177&y=409"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=177&y=410"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=177&y=411"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=178&y=408"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=178&y=409"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=178&y=410"
        ,"http://api.geoscore.com/dyntm/t/?ts=dtmUser:8F6C95E45B782AA26D1B7153A6FE8D59&z=10&x=178&y=411"
        ]

        start = time.time()
        #self.responses = grequests.map(unsentrequests, size=self.max_conn)
        self.responses = [ request.head(r) for r in TEST]
        delta = time.time() - start
        self.name2results[layername][roundidx, zoomidx] = delta
        print "Layer:", layername, "Zoom:", self.zooms[zoomidx], delta
        status = [ r.status_code for r in self.responses]
        percenterror=(len(status)-status.count(200))/len(status)*1.0
        if percenterror != 0:
            print "Warning found bad reponses returned by server!"
            print "Layer name: ", layername
            print "zoom: ", zoomidx
            print "% BAD responses",round(percenterror*100,2) 
            print "--------------------------------------------------"

=======
>>>>>>> 055823c53b81223b6ebe1cf0dfab11daef3ee042

        for roundidx in range(self.rounds):
            for zoomidx in range(len(self.zooms)):
                print "rounds: ", self.rounds
                print "zooms: ", self.zooms
                begin = roundidx*len(self.zooms)*self.TILE_SIZE**2+zoomidx*self.TILE_SIZE**2
                end = begin + self.TILE_SIZE**2
                urls = self.urls[begin:end]
                #if options.verbose:
                print "request batch being sent to server:"
                print "\n".join(urls)
                rsess = requests.session()
<<<<<<< HEAD
                unsentrequests = [grequests.head(l, session=rsess) for l in urls]
=======
                unsentrequests = [grequests.get(l, session=rsess) for l in urls]
>>>>>>> 055823c53b81223b6ebe1cf0dfab11daef3ee042
                start = time.time()
                self.responses = grequests.map(unsentrequests, size=self.max_conn)
                delta = time.time() - start
                self.name2results[layername][roundidx, zoomidx] = delta
                print "Layer:", layername, "Zoom:", self.zooms[zoomidx], delta
                status = [ r.status_code for r in self.responses]
                percenterror=(len(status)-status.count(200))/len(status)*1.0
                if percenterror != 0:
                    print "Warning found bad reponses returned by server!"
                    print "Layer name: ", layername
                    print "zoom: ", zoomidx
                    print "% BAD responses",round(percenterror*100,2) 
                    print "--------------------------------------------------"

    def deg2num(self, zoom, lat_deg, lon_deg):
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** int(zoom)
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    def buildrequests(self):
        urls=[]

        if os.path.isfile(self.request_pool) and self.request_pool.endswith('.csv'):
            # Assume this is a .csv from splunk and we are replaying the traffic.
            reader = csv.reader(open(self.request_pool, 'rb'), delimiter=',')
            header=reader.next()
            try:
                print header
                idx = header.index("api_request")
            except ValueError:
                print header
                print "ERROR: no api_request field in .csv file " + \
                      self.request_pool
                sys.exit(1)
            for row in reader:
                print row
                if not row:
                    continue
                a = row[idx]
                a = a.split("&jsonp")[0]
                parts = a.split("/")
                if options.api_key:
                    # Usually, we don't want to use random keys from logfiles.
                    if len(parts) > 3 and parts[2] != 'icons':
                        a = a.replace(parts[2], options.api_key)
                if "intersects" in a:
                    a = a.replace("\\","")
                    a = a.replace("\t","t")
                    a = a.replace('type:Point,coordinates','"type":"Point","coordinates"')
                if options.verbose:
                    print "QUEUING:", a
                urls.append(self.server + a)

        # keep functionality for Mapfluence requests while adding geoscore urls
        elif re.match(r'.*/\{z\}/\{x\}/\{y\}\.png.*', self.request_pool) or re.match(r'.*dtmUser.*', self.request_pool):
            for i in range(self.rounds):
                lat, lon = self.get_center()
                print "request name ", self.request_name
                if "ca" in self.request_name:
                    # Use Los Angeles as center of CA test
                    lat,lon =34.0500,-118.2500
                
                for zoom in self.zooms:
                    print "request name", self.request_name
                    print "center ", lat, lon
                    x, y = self.deg2num(zoom, lat, lon)
                    TILE_SIZE = self.TILE_SIZE
                    #TILE_SIZE = 7 # MAPFLUENCE TEST
                    XY = [(x0, y0) for x0 in range(x, x + TILE_SIZE) for y0 in range(y, y + TILE_SIZE)]
                    for xy in XY:
                        url = self.server + self.request_pool
                        url = url.replace("{APIKEY}", options.api_key)
                        url = url.replace("{OPACITY}", str(self.get_opacity()))
                        url = url.replace('{z}', str(zoom))
                        url = url.replace('{x}', str(xy[0]))
                        url = url.replace('{y}', str(xy[1]))
                        if options.verbose:
                            print "QUEUING:", url
                        urls.append(url)

        else:
            # assume this is a url with {VARIABLES}
            #if not self.request_pool.startswith('/'):
            #    print "Arbitrary URLs must start with a '/'"
            #    sys.exit(1)

            for i in range(self.rounds):
                lat, lon = self.get_center()
                url = self.server + self.request_pool
                # TODO: obviously have to come up with something better for
                # this.
                url = url.replace("{APIKEY}", options.api_key)
                url = url.replace("{LAT}",str(lat)).replace("{LON}",str(lon))
                if options.verbose:
                    print "QUEUING:", url
                urls.append(url)

        return urls

    def showprogress(self, response, **kwargs):
        self.progress = self.progress + 1 
        if response.status_code==200:
            self.statusok += 1
        elif 500<=response.status_code<600:
            self.statuserror += 1
        elif 400<=response.status_code<500:
            self.statusfail += 1
        sys.stdout.write("\r%d%% (%d of %d) \033[92m%d OK \033[93m%d FAILS \033[91m%d ERRORS\033[0m"%
                         ((float(self.progress)/float(len(self.urls)))*100,
                          self.progress,len(self.urls),
                          self.statusok,self.statusfail,self.statuserror))
        sys.stdout.flush()
        
    def asyncrun(self):
        urls=self.urls
        rsess = requests.session()
        #rsess.config['keep-alive'] = False
<<<<<<< HEAD
        unsentrequests = [grequests.head(l,hooks = {'response': self.showprogress },session=rsess) for l in urls]
=======
        unsentrequests = [grequests.get(l,hooks = {'response': self.showprogress },session=rsess) for l in urls]
>>>>>>> 055823c53b81223b6ebe1cf0dfab11daef3ee042
        self.responses=grequests.map(unsentrequests, size = self.max_conn)
        return self.responses

    def reporterrors(self):
        nerrors=len(self.errortypes)
        idx=0
        for mferror,uri in self.errortypes.items():
            idx=idx+1
            print str(idx) + " of " + str(nerrors)," types" ,"  ERROR : ",mferror," EXAMPLE REQUEST:  ", uri
            print "count of requests returning this type of error: " , self.errorpools[mferror].count
            print " ---------------------- "

    def asynclog(self):
        pool = ""
        pool += "======================================================================================\n"
        pool += "               Request pool of {{request_pool}} \n"
        pool += "======================================================================================\n"
        print ""
        print ""
        pool=pool.replace("{{request_pool}}",self.request_pool)
        for idx, r in enumerate(self.responses):
                if r.status_code == 200:
                    pass
                elif r.status_code == 403:
                    print "Status code: 403"
                    print "PROBLEM FIXER ====> Disable key auth in local_settings.py "
                    break
                else:
                    if idx==0: print pool
                    print "No.", idx
                    print ")-: Bad Request: ", r.url
                    print ""
                    print r.status_code, "Error: ", r.headers.get('x-mferror',"None Supplied")
                    print ""
                    print ""
                    print ""
                    print "---------------------------------------------------"
                    mferror = r.headers.get('x-mferror', "None Supplied")

                    # check if we already recorded that error
                    if mferror not in self.errorpools: 
                        self.errorpools[mferror]=Errorpool()
                        self.errorpools[mferror].count=1
                        self.errorpools[mferror].url=r.url
                        self.counterrortypes += 1
                        self.errorpools[mferror].erroridx = self.counterrortypes
                        idx=str(self.counterrortypes)
                        self.errorpools[mferror].log=open('errorpool_'+idx+'.log', 'w')
                        self.errorpools[mferror].log.write(r.url+"\n")

                    if mferror not in self.errortypes: 
                        self.errortypes[mferror]=r.url

                    if mferror in self.errorpools:
                        self.errorpools[mferror].count+=1
                        self.errorpools[mferror].log.write(r.url+"\n")
                        if len(self.errorpools[mferror].url)>r.url:
                            # use the shortest request as an example of the error
                            self.errorpools[mferror.url]=r.url

                    if mferror in self.errortypes and len(self.errortypes[mferror])>r.url:
                        self.errortypes[mferror]=r.url

    def print_stats(self):
        times = numpy.array([r.elapsed.total_seconds() for r in self.responses if hasattr(r, 'elapsed')])
        print "Mean fetch time: %fs (stddev: %fs)" % \
              (numpy.mean(times), numpy.std(times))
        print "Max fetch time: %fs" % numpy.max(times)
        errorsum = 0
        for errorv in self.errorpools.itervalues():
            errorsum += errorv.count
<<<<<<< HEAD
        print "Total Time: %fs" % round(self.end - self.start, 2)
=======
        print "Total Time to run all requests: %fs" % round(self.end - self.start, 2)
>>>>>>> 055823c53b81223b6ebe1cf0dfab11daef3ee042
        print "Types of Errors:", len(pool.errorpools.keys())
        print "Total Errors:", errorsum

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


if __name__ == '__main__':
    pool=Requestpool(zooms=options.zooms, center=options.center,
                     rounds=options.rounds, opacity=options.opacity,
                     max_conn=options.max_conn)
    r=pool.run()
    end=time.time()
    pool.print_stats()

    if options.file:
        print "Saving response data to", options.file
        f = open(options.file, "w")
        f.write("uri\tlatency\n")
        for r in pool.responses:
            f.write(r.request.path_url + '\t' +
                    str(r.elapsed.total_seconds()) + '\n')
        f.close()
