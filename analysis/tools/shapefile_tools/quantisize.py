import sys
import fiona
import glob
import datetime
import time
## 4 SEC
import logging
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(message)s' ' | ' '%(filename)s' ' line:' '%(lineno)d',
#                    filename='/mnt/quantize.log',
#                    filemode='w',
#                    datefmt='%a, %d %b %Y %H:%M:%S')


INPUT_FILENAME="/mnt/ca_FIELDS_EDITED.shp"
OUTPUT_FILENAME="/mnt/ca_3decimal.shp"
#INPUT_FILENAME="/mnt/blocks_zoom7_precision2decimal.shp"
#OUTPUT_FILENAME="/mnt/blocks_zoom3_precision1decimal.shp"
DECIMALS=3

#@profile
seen = set()
seen_add = seen.add
# GET the schema of the new shapefile from one of the old ones
records=[]
idx=0
with fiona.open(INPUT_FILENAME, 'r') as source:
    sink_schema = source.schema.copy()
    sink_driver=source.driver

        # Make a new one 
    with fiona.open(
        OUTPUT_FILENAME, 'w',
	crs=source.crs,
        driver=sink_driver,
        schema=sink_schema,
	) as sink:


            records=[]

            start=time.time()
	    source_count = len(source)
	    print "count: " , source_count
	    for j,feature in enumerate(source):
			if j % 5000==0:
                        #print j
			#if j % 100==0:
			    #print "id: ",feature['id'],"enumerate: ", j
		            completed=float(j+1)/(source_count) * 100.0
			    delta=time.time()-start
			    sys.stdout.write("\r{progress} portion done in {mins} s".format(progress=completed,mins=delta))
			    sys.stdout.flush()

			newshapes=[]
			shapes=feature["geometry"]["coordinates"]
			#print "len(shapes) ",len(shapes) 
			if feature["geometry"]['type']!='MultiPolygon':
                                #print "multipoly"
				for shape in shapes:
				    #newshape=[]
                                    #print "pt in shape"
                                    #print "len(shape)", len(shape)
                                    #print "shape", shape
				    newshape=[(round(pt[0],DECIMALS),round(pt[1],DECIMALS)) for pt in shape]
			            smallershape = [ x for x in newshape if x not in seen and not seen_add(x)]
				    seen.clear()
				      
				    if len(smallershape) < 3: # shape too small
					#print "Warning: too small a shape"
					newshapes.append(newshape[:4]) # just add same points 
				    else:
					newshapes.append(smallershape)
				    del smallershape
				    del newshape
			else:
				for shape in shapes:
                                    #print "single polys with ring holes"
				    newshape=[]
				    for ring in shape:
					    newring=[(round(pt[0],DECIMALS),round(pt[1],DECIMALS)) for pt in ring]
					    smallerring = [ x for x in newring if x not in seen and not seen_add(x)]
					    seen.clear()
					    if len(smallerring) < 3: # shape too small
						#print "Warning: too small a ring"
						newshape.append(newring[:4]) # just add same points 
					    else:
						newshape.append(smallerring)
					    del smallerring 
					    del newring 
				    newshapes.append(newshape)
				    del newshape

			feature["geometry"]["coordinates"]=newshapes
			del newshapes
			records.append(feature)
			#sink.write(feature)
			if j % 100==0:
			    sink.writerecords(records)
			    sink.flush()
			    del records[:] 

	    sink.writerecords(records)
	    sink.flush()



if __name__=="__main__":
    pass
    #try:
    #    main()
    #except:
    #    logging.exception('')
    #    import sys
    #    sys.exit()
