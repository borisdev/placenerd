import time
import rtree
#from util import shapefile
import pysal
from pysal.core.util import shapefile

EPS = 0.00001

class BBoxLocator(object):
    """
    area_contains_point() will return the one census area containing the point, and will take 15X longer about

    contains_point() will return a list of areas whose bonding boxes contain the point, and is much faster 
    """
    def __init__(self, shp_name):
        shp = shapefile.shp_file(shp_name,'r')
        idx = rtree.index.Index()

        data = {}
        for i,rec in enumerate(shp):
            bb = (rec['BBOX Xmin'], rec['BBOX Ymin'], rec['BBOX Xmax'], rec['BBOX Ymax'])
            data[i] = bb
            idx.insert(i, bb)
        self.idx = idx
        self.data = data
        self.pysalshp=pysal.open(shp_name,'r')
    def contains_point(self,pt):
        x,y = pt
        left = x - EPS
        right = x + EPS
        bottom = y - EPS
        top = y + EPS
        return list(self.idx.nearest((left,bottom,right,top)))
    def area_contains_point(self,pt):
        x,y = pt
        left = x - EPS
        right = x + EPS
        bottom = y - EPS
        top = y + EPS
        potentials=list(self.idx.nearest((left,bottom,right,top)))
        for o in potentials:
            if self.pysalshp.get(o).contains_point(pt)==1:
                return o

if __name__=='__main__':
    import time
    t0 = time.time()
    loc = BBoxLocator('../data/2602F1384BA06F1C6F68E9A6676CDA1A.shp')
    t1 = time.time()
    print 'built in:', t1-t0
    x,y,X,Y = loc.data[0]
    qx = (X+x) / 2.0
    qy = (Y+y) / 2.0
    pt = (qx,qy)
    print loc.area_contains_point(pt)

