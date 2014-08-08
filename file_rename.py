'''
author   : Joy Rahman
function : This script does bulk renaming
'''
import os
import sys

run_ok = False
if len(sys.argv) == 5:
    directory_name = sys.argv[1]
    old_extension = sys.argv[2]
    name_pattern  = sys.argv[3]
    new_extension = sys.argv[4]
    print "Running jobs on directory: {} having extensions {}".format(directory_name, old_extension)
    run_ok = True

else:
    print "SYNTAX : python file_rename.py directory_name matching_extension new_name_pattern new_extension"
    pass

if (run_ok):
    list = os.listdir( directory_name )
    counter = 1
    for old_file in list:
        if old_extension in old_file:
            new_file = name_pattern + str( counter ) + "." + new_extension
            os.rename( directory_name + "/"+ old_file, directory_name + "/" + new_file )
            print "file renamed from {} to {}".format( old_file, new_file )
            counter += 1
