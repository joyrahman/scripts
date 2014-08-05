#!/usr/bin/env python
 
import requests
import json
import sys
import os
 
def get_url_and_token():
	user = os.getenv('ST_USER', None)
	auth = os.getenv('ST_AUTH', None)
	key = os.getenv('ST_KEY', None)
 
	if not (user and auth and key):
		print 'must supply ST_USER, ST_AUTH and ST_KEY env vars'
		sys.exit(1)
 
	res = requests.get(auth, headers={'x-storage-user': user,
					'x-storage-pass': key})
 
	return(res.headers.get('x-storage-url', None),
		res.headers.get('x-auth-token', None))
 
 
def zebra_execute(endpoint, token, manifest):
	return requests.post(
		endpoint,
		headers={
			'X-Auth-Token': token,
			'Content-Type': 'application/json',
			'X-ZeroVM-Execute': '1.0',
			'X-Zerovm-Deferred': 'always'},
		data=manifest)
 
 
def get_object(endpoint, token, container, object):
	resp = requests.get(
		"%s/%s/%s" % (endpoint, container, object),
		headers={'X-Auth-Token': token})
 
	if resp.status_code != 200:
		sys.stderr.write('Result code %d getting json file' % resp.result_code)
 
	return resp.content
 
 
def usage():
	print 'zexec <local file> or zexec <container> <job>'
	sys.exit(1)
 
# either run as 'zexec <local file>' or zexec <container> <job>'
json_file = ''
url, token = get_url_and_token()
 
if len(sys.argv) == 2:
	with open(sys.argv[1], 'r') as f:
		json_file = f.read()
elif len(sys.argv) == 3:
	container = sys.argv[1]
	obj = sys.argv[2]
	json_file = get_object(url, token, container, obj)
else:
	usage()
 
resp = zebra_execute(url, token, json_file)
 
print resp.content
