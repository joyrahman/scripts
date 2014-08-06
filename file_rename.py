'''
author   : Joy Rahman
function : This script does bulk renaming
'''
import os
import sys

if len(sys.argv) == 3:
    directory_name = sys.argv[1]
    file_extension = sys.argv[2]
    name_pattern  = sys.argv[3]
    print "Running jobs on directory: {} having extensions {}".format(directory_name, file_extension)

else
    print "python file_rename.py directory_name file_extension name_pattern"

list = os.listdir( directory_name )
counter = 1
for old_file in list:
    if file_extension in old_file:
        new_file = "test_"+ str( counter ) + ".txt"
        os.rename( directory_name + "/"+ old_file, directory_name + "/" + new_file )
        print "file renamed from {} to {}".format( old_file, new_file )
        counter += 1
