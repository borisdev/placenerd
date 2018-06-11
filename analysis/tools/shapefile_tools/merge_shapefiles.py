import sys
import fiona
import glob
import datetime

OUTPUT_FILENAME="/mnt/blocks.shp"

filenames=[filename for filename in glob.glob('../*.shp')]
# Below cant run until i fix CA DBF -- DONE 
filenames=["/mnt/merge_ca_ct_rest/blocks_minus_ca_ct/merged_blocks_final.shp", # 3.2GB
           "/mnt/merge_ca_ct_rest/ca/ca_FIELDS_EDITED.shp",
           "/mnt/merge_ca_ct_rest/ct/ct_Export_Output.shp"
          ]
# Below is 2.1 GB
#filenames=["/vol/block_trimmed_shapefiles/tl_2010_48_tabblock10_trimmed.shp", # 710 MB
#           "/mnt/merge_ca_ct_rest/ca/ca_FIELDS_EDITED.shp" # 600 MB
#          ]
#filenames=[
#        "/vol/block_trimmed_shapefiles/tl_2010_13_tabblock10_simplified_trimmed.shp",
#        "/vol/block_trimmed_shapefiles/tl_2010_29_tabblock10_simplified.shp",
#        "/vol/block_trimmed_shapefiles/tl_2010_36_tabblock10_simplified_trimmed.shp",
#        "/vol/block_trimmed_shapefiles/tl_2010_34_tabblock10_simplified_trimmed.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_25_tabblock10_simplified_trimmed.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_42_tabblock10_simplified_trimmed.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_17_tabblock10_simplified_trimmed.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_12_tabblock10_simplified_trimmed.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_19_tabblock10_simplified.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_18_tabblock10_simplified_trimmed.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_20_tabblock10_simplified.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_02_tabblock10_simplified.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_05_tabblock10_simplified.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_40_tabblock10_simplified.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_04_tabblock10_simplified.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_39_tabblock10_simplified_COPY_trimmed.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_01_tabblock10_simplified_trimmed.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_26_tabblock10_simplified_trimmed.shp",
#	"/vol/block_trimmed_shapefiles/tl_2010_48_tabblock10_trimmed.shp"
#          ]

# GET the schema of the new shapefile from one of the old ones
with fiona.open(filenames[0], 'r') as source:
    sink_schema = source.schema.copy()
    sink_driver=source.driver
# Make a new one 
with fiona.open(
    #'/mnt/merged_blocks_final_with_ca_ct.shp', 'w',
    OUTPUT_FILENAME, 'w',
    crs=source.crs,
    driver=sink_driver,
    schema=sink_schema,
    ) as sink:

    for i,filename in enumerate(filenames):
        print i+1,"of",len(filenames), filename
        start=datetime.datetime.now()
        with fiona.open(filename, 'r') as source:
            #assert sink_schema==source.schema, "cant merge since different dbf schemas"
            big=set(sink_schema["properties"].keys())
            small=set(source.schema["properties"].keys())
            print source.schema["properties"].keys()
            print "diff between 1st shp and this one's db properties:"
            print big-small
            assert len(big-small)==0
            source_count = len(source) 
            print "count: " , source_count
            for j,feature in enumerate(source):
                sink.write(feature)
                completed=float(j)/float(source_count) * 100.0
                if j % 1000==0:
                    delta=datetime.datetime.now()-start
                    sys.stdout.write("\r{progress} portion done".format(progress=completed))
                    sys.stdout.flush()

