import sys
import pysal
def print_usage():
    print "Usage: python rename_dbf_col.py OLD_COL_NAME NEW_COL_NAME old.dbf new.dbf"

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
