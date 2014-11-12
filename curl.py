#export OS_STORAGE_URL=`python curl.py storage_url`
#export OS_AUTH_TOKEN=`python curl.py auth_token`


import requests
import sys

url = 'http://127.0.0.1:8080/auth/v1.0'
header_parameters = {'x-Auth-User':'admin:admin','x-Auth-Key':'Wahv4quewi2me3'}
r =  requests.get(url, headers = header_parameters)
#print r.text
#print r.headers


storage_url = r.headers['X-Storage-Url']
auth_token = r.headers['X-Auth-Token']

#os.environ['OS_STORAGE_URL'] = '{}'.format(str(r.headers['X-Storage-Url']))
#os.environ["OS_AUTH_TOKEN"]  = str(r.headers['X-Auth-Token'])

if len(sys.argv) > 0:
   if sys.argv[1] == "storage_url":
	print storage_url
   elif sys.argv[1] == "auth_token":
        print auth_token
