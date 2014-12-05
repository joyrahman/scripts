import urllib2
import requests
import sys
import os
import json
container_name = "movie"
container_url= os.environ['OS_STORAGE_URL'] + "/" + container_name
auth_token = os.environ['OS_AUTH_TOKEN']

header_parameters = { 'X-Auth-Token': '{}'.format(auth_token)}
#print os.environ['OS_AUTH_TOKEN']

directory_list = requests.get( container_url,  headers = header_parameters)
#output = open('test.mp3','wb')
#output.write(mp3file.read())
#output.close()
listing = str(directory_list.text).split("\n")
listing =  filter(None, listing)
i = 0 
for item in listing:
    print "{}".format(i)+ ":" +item
    i += 1
    request_string = urllib2.Request(container_url + "/"+item, headers=header_parameters)
    remote_fp =  urllib2.urlopen(request_string)
    output = open(item, 'wb')
    output.write(remote_fp.read())
    output.close()

    

#for each item in the listing, copy the file and write back to a location with the same name 


#a=directory_list.json

#print a.__dict__
#for item in directory_list.text:
#    print item
#print directory_list.text[0]
#print type(directory_list.text)

