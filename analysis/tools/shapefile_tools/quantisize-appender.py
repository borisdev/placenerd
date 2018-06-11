import sys
import fiona
import glob
import datetime

## 4 SEC
import logging
#logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(message)s' ' | ' '%(filename)s' ' line:' '%(lineno)d',
#                    filename='/mnt/quantize.log',
#                    filemode='w',
#                    datefmt='%a, %d %b %Y %H:%M:%S')


OUTPUT_FILENAME="/mnt/blocks_zoom7_precision2decimal.shp"
#OUTPUT_FILENAME="/mnt/blocks_zoom3_precision1decimalTEST.shp"
INPUT_FILENAME="/mnt/blocks_zoom10precision.shp"

#@profile
def main():
        seen = set()
        seen_add = seen.add
	# GET the schema of the new shapefile from one of the old ones
        records=[]
        idx=0
	with fiona.open(INPUT_FILENAME, 'r') as source, fiona.open(OUTPUT_FILENAME, 'a') as sink:
		    source_count = float(len(source))
		    sink_count = float(len(sink))
		    print "source count: " , source_count
		    print "sink count: " , sink_count
	            start=datetime.datetime.now()

                    #while idx<1000:
                    #    idx+=1
                    #    f=source.next()
	            #end1=datetime.datetime.now()
                    #delt=end1-start
                    #print "----------------------"
                    #print delt.microseconds, "msecs"
                    #sys.exit()

                    for j,feature in enumerate(source):


			if j+1 > sink_count: 
				#if j % 5000==0:
				if j+1-sink_count % 1000==0:
				    #print "id: ",feature['id'],"enumerate: ", j
				    completed=(float(j+1)-sink_count)/(source_count-sink_count) * 100.0
				    delta=datetime.datetime.now()-start
				    #mins=(delta.seconds)/60.0
				    mins=(delta.seconds)
				    #sys.stdout.write("\r{progress} portion done in {mins} mins".format(progress=completed,mins=mins))
				    sys.stdout.write("\r{progress} portion done in {mins} s".format(progress=completed,mins=mins))
				    sys.stdout.flush()

				newshapes=[]
				shapes=feature["geometry"]["coordinates"]
				#print len(shapes)
				if feature["geometry"]['type']!='MultiPolygon':
					for shape in shapes:
					    #newshape=[]
					    for pt in shape:
						#newshape=[(round(pt[0],PRECISION),round(pt[1],PRECISION)) for pt in shape]
						newshape=[(round(pt[0],2),round(pt[1],2)) for pt in shape]
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
					    newshape=[]
					    for ring in shape:
						    newring=[(round(pt[0],2),round(pt[1],2)) for pt in ring]
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
		        elif j % 1000==0:
		            sys.stdout.write("\r{j} {sink_count}".format(j=j,sink_count=sink_count))
		            sys.stdout.flush()

                    sink.writerecords(records)
		    sink.flush()



if __name__=="__main__":
    main()
    #try:
    #    main()
    #except:
    #    logging.exception('')
    #    import sys
    #    sys.exit()
