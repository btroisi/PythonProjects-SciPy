# Stephanie Taylor
# Spring 2014
# Test the Data class's ability to store and return information about the raw data
import sys
import data

def test_raw_data( filename ):
    print "\n Testing the fields and acessors for raw data\n"
    d = data.Data( filename )
    headers = d.get_raw_headers()
    print "d.get_raw_headers()"
    print d.get_raw_headers()
    print "d.get_raw_type"
    print d.get_raw_type()
    print "d.get_raw_num_columns"
    print d.get_raw_num_columns()
   

    try:
        print "d.get_num_rows\n", d.get_num_rows()
    except:
        print "class has no method get_num_rows()"

    try:
        print "d_get_num_raw_rows\n", d.get_num_raw_rows()
    except:
        print "class has no method get_num_raw_rows()"

    print "d.get_raw_row(1)"
    print d.get_raw_row(1)
    print "type( d.get_raw_row(1) )"
    print type( d.get_raw_row(1) )
    print "d.get_raw_value(0,headers(1))"
    print d.get_raw_value(0,headers[1])
    print "type(d.get_raw_value(0,headers(1)))"
    print type(d.get_raw_value(0,headers[1]))
    print "d.get_headers"
    print d.get_headers()
    print "d.get_num_columns"
    print d.get_num_columns()
    print "d.get_row(1)"
    print d.get_row(1)
    print "d.get_value(0,headers[2])"
    print d.get_value(0,headers[2])
    print "d.get_data(headers[1])"
    #print d.get_data(0,headers[1])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python %s <csv_filename>" % sys.argv[0]
        print "       where <csv_filename> specifies a csv file"
        exit()
    test_raw_data( sys.argv[1] )
