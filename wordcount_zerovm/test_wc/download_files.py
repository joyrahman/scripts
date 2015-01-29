from webhdfs.webhdfs import WebHDFS
import urllib2
import requests
import sys
import os, tempfile
import json
import subprocess
import time
import logging


'''
python download_file.py [source_container] [filepattern]
'''

# logging configuration
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('time.log')
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

#### START OF EXECUTION  #####
logger.info('execution started')


# webhdfs : http://hadoop.apache.org/docs/r1.0.4/webhdfs.html
#hdfs_server_name = "localhost"
#hdfs_server_port = 50070
#hdfs_user_name = "ubuntu"
#webhdfs = WebHDFS(hdfs_server_name, hdfs_server_port , hdfs_user_name)
# swift parameters
#container_name = "movie"
container_name = sys.argv[1]

file_pattern = None
if len(sys.argv) >= 2:
    file_pattern = sys.argv[2]

#executable_mapper = sys.argv[2]
#executable_reducer = sys.argv[3]
#executable_jar = "/usr/local/hadoop-1.2.1/contrib/streaming/hadoop-*streaming*.jar"
container_url= os.environ['OS_STORAGE_URL'] + "/" + container_name
auth_token = os.environ['OS_AUTH_TOKEN']
header_parameters = { 'X-Auth-Token': '{}'.format(auth_token)}


# Connect to the Swift Server
directory_list = requests.get( container_url,  headers = header_parameters)
#output = open('test.mp3','wb')
#output.write(mp3file.read())
#output.close()
listing = str(directory_list.text).split("\n")
listing = filter(None, listing)
if len(sys.argv) >= 2:
    listing = filter(lambda s: s.endswith(file_pattern),listing)
i = 0 
# create the container at hdfs
#hdfs_target_path = "/usr/" + hdfs_user_name + "/" + container_name
#webhdfs.mkdir(hdfs_target_path)

print listing

for item in listing:
    print "{}".format(i)+ ":" +item

    i += 1
    request_string = urllib2.Request(container_url + "/"+item, headers=header_parameters)
    remote_fp =  urllib2.urlopen(request_string)
    output = open(item, 'wb')
    output.write(remote_fp.read())
    output.close()
    #local_path = os.getcwd()+"/"+item
    #print local_path, " -> ", hdfs_target_path 
    #webhdfs.copyFromLocal(local_path,hdfs_target_path+"/"+item)
    #target_file = hdfs_target_path+"/"+item
    #command_str = 'hadoop fs -copyFromLocal {} {}'.format(local_path,target_file)
    #print command_str
    #p = subprocess.Popen( command_str , shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #for line in p.stdout.readlines():
    #    print line
    #retval = p.wait()
    #print retval

    # Execute the job
#input_dir =  hdfs_target_path
#output_dir = hdfs_target_path + "/out"
'''
command_str = "hadoop jar {} \
     -file {}    -mapper {} \
     -file {}   -reducer {} \
     -input {} -output {}".format(executable_jar,executable_mapper, executable_mapper,executable_reducer,executable_reducer,input_dir,output_dir)
p = subprocess.Popen( command_str , shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print line
retval = p.wait()
print retval 

#cmd = 'hadoop fs -copyFromLocal {} '
#p = subprocess.Popen('ls', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#for line in p.stdout.readlines():
#    print line,
#retval = p.wait()    

#for each item in the listing, copy the file and write back to a location with the same name 


#a=directory_list.json

#print a.__dict__
#for item in directory_list.text:
#    print item
#print directory_list.text[0]
#print type(directory_list.text)
'''
