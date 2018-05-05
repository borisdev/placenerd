import sys
import fiona
import glob
import datetime

OUTPUT_FILENAME="/mnt/blocks_zoom3precision1decimal.shp"
INPUT_FILENAME="/mnt/blocks_zoom7_precision2decimal.shp"
#INPUT_FILENAME="/mnt/blocks.shp"
PRECISION=1 # DECIMALS PLACES


def uniquify(seq):
    #http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

#@profile
def main():
	# GET the schema of the new shapefile from one of the old ones
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

		start=datetime.datetime.now()
		with fiona.open(INPUT_FILENAME, 'r') as source:
		    source_count = len(source) 
		    print "count: " , source_count
		    for j,feature in enumerate(source):
			if j==6000: break

			completed=float(j)/float(source_count) * 100.0
			if j % 1000==0:
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
				    newshape=[]
				    for pt in shape:
					newshape.append((round(pt[0],PRECISION),round(pt[1],PRECISION))) # reduce precision
				    smallershape=uniquify(newshape)
				    if len(smallershape) < 3: # shape too small
					#print "Warning: too small a shape"
					newshapes.append(newshape[:4]) # just add same points 
				    else:
					newshapes.append(smallershape)
			else:
				for shape in shapes:
				    newshape=[]
				    for ring in shape:
					    newring=[]
					    for pt in ring:
						newring.append((round(pt[0],PRECISION),round(pt[1],PRECISION))) # reduce precision
						smallerring=uniquify(newring)
						if len(smallerring) < 3: # shape too small
						    #print "Warning: too small a ring"
						    newshape.append(newring[:4]) # just add same points 
						else:
						    newshape.append(smallerring)
				    newshapes.append(newshape)

			feature["geometry"]["coordinates"]=newshapes
			sink.write(feature)



if __name__=="__main__":
    main()
