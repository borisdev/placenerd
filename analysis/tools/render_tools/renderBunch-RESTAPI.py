import urllib
import time


url = "http://127.0.0.1/dyntm/t?ts=dtmUser:2602F1384BA06F1C6F68E9A6676CDA1A&z=%d&x=%d&y=%d&b=0&cl=dtmUser:b6c9c590613a54471ab1b2730b397ac4&cs=dtmUser:1fa612b4e5b792aafcc8c18088b33f88"


for zoom in range(5,14):
	xr = (1+zoom)**2
	for x in xrange(xr):
		for y in xrange(xr):
			u = url%(zoom,x,y)
			t0 = time.time()
			c = urllib.urlopen(u)
			n = len(c.read())
			t1 = time.time()
			print "Got Tile: (z%d, x%d, y%d) in %0.5f seconds, %d bytes"%(zoom,x,y,t1-t0, n)

