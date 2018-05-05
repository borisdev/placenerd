"""write census values to a .h5 file

    Arguments:
              shapefilename.dbf   contains geoids of areas for which want values
              variableid          the census code for the attribute you want
              newfile.h5          name of the output .h5 file

    why? ... because using pyTable to access a specific variables.hd5 file works nicely with numpy 
"""
import sys
import numpy
import pysal
import pyACS
from tables import *

def print_usage():
    print "Usage: python census2table.py geoids.dbf variableid newfile.h5"

if __name__ == '__main__':

    if len(sys.argv) != 5:
        print_usage()
    else:
        a,b,ifname,ofname = sys.argv[1:]
        print a,b,ifname,ofname
        assert ifname.split(".")[-1]=="dbf", " input file must be a .dbf"
        assert ofname.split(".")[-1]=="dbf", "output file must be .dbf"
        if ifname.lower() == ofname.lower():
            print "Cannot overwrite the DBF we are reading from, please choose a new name for the output"
            sys.exit(1)
        if ifname.lower().endswith('.dbf') and ofname.lower().endswith('.dbf'):
            i = pysal.open(ifname, 'r')
            print i.header
            try:
                idx = i.header.index(a)
            except ValueError:
                print "%s does not appear to be a valid column name in %s"%(a,ifname)
                print "The valid columns are:", i.header
                sys.exit(1)
            if b in i.header:
                print "Cannot reanem %s to %s, would result in 2 columns with same name"%(a,b)
            new_header = i.header[:]
            new_header[idx] = b
            
            o = pysal.open(ofname, 'w')
            o.field_spec = i.field_spec
            o.header = new_header
            for j, row in enumerate(i):
                print j
                o.write(row)
            o.close()
            i.close()

# Extract using Charlie's ACH 
dbf = pysal.open('/pyacs/tracts11.dbf')
geoids = dbf.by_col('GEOID') # shapefile geoid, 11chars=2state+3county+6tract
datasetObj = pyACS.ACS()
tract_total = numpy.array(datasetObj.get_ordered(geoids, 'B01003001'))
tract_black = numpy.array(datasetObj.get_ordered(geoids, 'B02009001'))
N=len(tract_black)

# Define a pyTable's record that describes a census tract
class TractModel(IsDescription):
    geoid           = StringCol(11)   # geoid
    blackcount        = UInt16Col()     # Unsigned short integer
    tractcount        = UInt16Col()     # Unsigned short integer

filename = "census_variables.h5"
h5file = open_file(filename, mode = "w", title = "Census Variables")
group = h5file.create_group("/", 'tracts', 'Tract Level')# new group under "/" (root)
tract_race_table = h5file.create_table(group, 'readout', TractModel, "Race Counts")# new table of group
# Fill the table with 10 particles
tract = tract_race_table.row
for i in xrange(N):
    tract_race_table.row['geoid']  = geoids[i]
    tract_race_table.row['blackcount'] = tract_black[i]
    tract_race_table.row['tractcount'] = tract_total[i]
    tract.append()
# Close (and flush) the file
h5file.close()
