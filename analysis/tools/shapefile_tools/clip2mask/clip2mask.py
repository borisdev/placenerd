import pysal
from pysal.contrib import shapely_ext
import shapely.geometry
import pysal.cg.rtree as rtree
import sys

def clip2mask(shapes, mask):
    if len(mask) > 1:
        raise NotImplementedError, "clip2mask does not yet support masks with more than one shape. Seperate your maskes into multiple shapefiles and run them one at a time."
    mask = mask.read()[0]
    index = rtree.Rtree()
    print "Building Spatial Index"
    cur_id = 0
    for ring in mask.parts:
        ### Build of segments
        # given ring = [A, B, C, D, A] <- rings should be closed
        # ring[:-1] = [A, B, C, D]
        #              |  |  |  |
        # ring[1:]  = [B, C, D, A]
        # Line Segments are [(AB, BC, CD, DA)]
        #
        if ring[0] != ring[-1]: raise ValueError, "A ring in mask polygon is not closed!"
        a = ring[:-1]
        b = ring[1:]
        for segment in zip(a,b):
            bbox = list(pysal.cg.get_bounding_box(segment))

            #bouding box of verticle and horizontal lines have no area,
            #not good for rtree, lets add some small area
            if bbox[0] - bbox[2] == 0:
                bbox[0] -= 0.001
                bbox[2] += 0.001
            if bbox[1] - bbox[3] == 0:
                bbox[1] -= 0.001
                bbox[3] += 0.001

            #print "adding",cur_id
            index.add(cur_id, bbox)

            #not sure of this is needed, might be able to use the same if for all segments,
            #but this is probably safer
            cur_id += 1
    print "...index built"
    n = len(shapes)
    for cur,shape in enumerate(shapes):
        # if index.intersection returns anything, the shape "might" intersect
        # the mask.  If it returns nothing, the shape if either
        # 1. contained by the mask.
        # 2. outside the mask.
        # for now we can ignore #2, if the shape is outside of the mask we'll include it.
        # in the future we can see if a QuadTree would help here.
        hittest = index.intersection(shape.bounding_box)
        if (hittest):
            print "clipping %d of %d"%(cur+1, n)
            try:
                if shapely_ext.intersects(mask,shape):
                    yield shapely_ext.intersection(mask, shape) #find intersection with mask
                else:
                    #in this case, the bounding boxes touch, but the shape exists outside
                    # the mask, the result would be an empty polygon
                    yield shape
            except Exception as e:
                print "An Exception occured durring intersection, yielding original"
                yield shape
        else:
            print "yielding %d of %d"%(cur+1, n)
            yield shape
if __name__ == '__main__':
    def print_usage():
        print "Usage: python clip2mask.py input.shp mask.shp output.shp"
    if len(sys.argv) != 4:
        print_usage()
    else:
        inshp = sys.argv[1]
        mask = sys.argv[2]
        outshp = sys.argv[3]
        if not (inshp.lower().endswith('.shp') and mask.lower().endswith('.shp') and outshp.lower().endswith('.shp')):
            print_usage()
            sys.exit(0)

        i = pysal.open(inshp, 'r')
        m = pysal.open(mask, 'r')
        oshp = pysal.open(outshp,'w')
        n = len(i)
        cur = 1
        for shape in clip2mask(i,m):
            cur += 1
            oshp.write(shape)
        oshp.close();
        
