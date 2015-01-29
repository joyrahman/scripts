#!/usr/bin/env python
import billing_report
import requests
import json
import sys
import os
import random
import time

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
            'X-ZeroVM-Execute': '1.0'},
            #'X-Zerovm-Deferred': 'always'},
        data=manifest)
 
 
def get_object(endpoint, token, container, object):
    resp = requests.get(
        "%s/%s/%s" % (endpoint, container, object),
        headers={'X-Auth-Token': token})
 
    if resp.status_code != 200:
        sys.stderr.write('Result code %d getting json file' % resp.result_code)
 
    return resp.content


def print_resp(resp,job_no):
    #print resp.content
    #print resp.headers.__dict__
    print resp.headers.__dict__
    print "\nJob {}\n".format(job_no)
    cdr =  resp.headers['X-Nexe-Cdr-Line']
    total, session_data = cdr.split(',',1)
    print "total_time:", total
    session_data = session_data.split(',')
    i = 0
    for item in session_data:
        if i%2 == 0:
            pass
            #print "session_time: ",item
        i += 1


def print_report(resp, job_no):
    #x-nexe-system
    #x-nexe-error
    #x-nexe-cdr-line
    #x-nexe-status
    sessions_id     = resp['x-nexe-system']
    sessions_error  = resp['x-nexe-error']
    sessions_status = resp['x-nexe-status']
    sessions_cdr    = resp['x-nexe-cdr-line']
    billing_report.get_billing_report(sessions_id, sessions_error, sessions_status, sessions_cdr)

def json_print(resp, job_no):
    print "job#{}".format(job_no)
    print json.dumps(resp.headers.__dict__, indent=2)
    print resp.__dict__

def usage():
    print 'automate_script.py <container_name> <json_name> <interval> <no_of_sessions>'
    sys.exit(1)




def main():


    json_file = ''
    url, token = get_url_and_token()

    ## user defined params

    obj = [ "wordcount_20.json" , "wordcount_80.json" ]
    popularity_factor = 80
    resp_list = []
    manifest_dir = "manifest"


    # usage : python automate_job.py <interval> <no_of_sessions>
    if len(sys.argv) == 3:
        interval = int(sys.argv[1])
        no_of_sessions = int(sys.argv[2])

        for i in range(0, no_of_sessions):
            x =  random.randrange(0,99)
            if x<= popularity_factor:
                json_file = get_object(url, token, manifest_dir, obj[0])
            else:
                json_file = get_object(url, token, manifest_dir, obj[1])
            #execute the job
            resp = zebra_execute(url, token, json_file)
            resp_list.append(resp)
            time.sleep(interval)

    elif len(sys.argv) == 1:
        manifest_dir = "debug"
        json_file = get_object(url, token, manifest_dir , obj[0])
        resp = zebra_execute(url, token, json_file)
        resp_list.append(resp)

    else:
        usage()

    jobcounter = 1
    for item in resp_list:
        #print_resp (item,jobcounter)
        json_print(item, jobcounter)
        #print_report(item, jobcounter)
        jobcounter += 1
#resp = zebra_execute(url, token, json_file)

#print type(resp)
#print type(resp.__class__.__dict__)

#print resp()
#for x in iter(resp):
#    print x

#print dir(resp.headers)
#print resp.__dict__ 
#print resp.content
#print resp.text
#print resp.headers.__dict__


'''
X-Nexe-Cdr-Line

Contains an accounting report from ZeroVM execution report.

Example:

    X-Nexe-Cdr-Line: 4.251, 3.994, 0.11 3.53 1262 75929984 34 199 0 0 0 0
    Note: current accounting stats format is:

    <ttotal>, <tnode>, <node_acc>, <tnode>, <node_acc>, <tnode>, <node_acc>,.....
    where:

    <ttotal> - total time, sec
    <tnode> - total node time, sec
    <node_acc> - node accounting line
    Note: current node accounting line format is:

    <sys> <user> <reads> <rbytes> <writes> <wbytes> <nreads> <nrbytes> <nwrites> <nwbytes>
    where:

    <sys> - system time, sec
    <user> - user time, sec
    <reads> - reads from disk
    <rbytes> - read bytes from disk
    <writes> - writes to disk
    <wbytes> - written bytes to disk
    <nreads> - reads from network
    <nrbytes> - read bytes from network
    <nwrites> - writes to network
    <nwbytes> - written bytes to network
'''
#print "Status: " + resp.headers['X-Nexe-System']
#print "CDR:" + resp.headers['X-Nexe-Cdr-Line']


#print resp.getheader('X-Nexe-System')
#for key in resp.headers.keys():
#    print key
#print json.dumps(resp.headers)
#for k,v,* in resp.headers:
#    print k, "->", v

#print cdr.__dict__

#print resp.header


if __name__ == '__main__':
    main()

