#!/usr/bin/env python
import billing_report
import requests
import json
import sys
import os
import random
import time
import threading
import logging

logging.basicConfig(level=logging.DEBUG,\
        format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

resp_list = []
def worker(url, token, json_file, job_id):
    global resp_list
    logging.debug("running the job")
    try:
        resp = zebra_execute(url,token,json_file)
        #resp_list.append(resp)
        #print_report(resp)
    except Exception as Inst:
        logging.debug ("Got some Error as worker>>",Inst)
    finally:
        #print_report(resp)
        print_resp(resp,job_id)




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
    print resp.headers['x-nexe-cdr-line']
    print resp.headers['x-nexe-status']
    #for key in resp.headers.keys():
    #    print "job:",job_no, key
    #print resp.headers['X-Nexe-Cdr-Line']
    #print resp.headers.__dict__
    #print "\nJob {}\n".format(job_no)
    #cdr =  resp.headers['X-Nexe-Cdr-Line']
    #total, session_data = cdr.split(',',1)
    #print "total_time:", total
    #session_data = session_data.split(',')
    #i = 0
    #for item in session_data:
     #   if i%2 == 0:
     #       pass
            #print "session_time: ",item
     #   i += 1


def print_report(resp, job_no=''):
    #x-nexe-system
    #x-nexe-error
    #x-nexe-cdr-line
    #x-nexe-status
    #print resp.__dict__
    print("###",job_no,"###")
    sessions_id     = resp.headers['x-nexe-system']
    sessions_error  = " "
    if 'x-nexe-error' in resp.headers:
        sessions_error  = resp.headers['x-nexe-error']
    sessions_status = resp.headers['x-nexe-status']
    sessions_cdr    = resp.headers['x-nexe-cdr-line']
    billing_report.get_billing_report(sessions_id, sessions_error, sessions_status, sessions_cdr)
    # print "-------------"
    # for item in report:
    #     print item, "\n"
    # print "-------------"

def json_print(resp, job_no):
    print "job#{}".format(job_no)
    print json.dumps(resp.headers.__dict__, indent=2)
    #print resp.__dict__

def usage():
    #print 'automate_script.py <container_name> <json_name> <interval> <no_of_sessions>'
    print 'python automated_job2.py {interval} {no_of_sessions} {popularity}'
    sys.exit(1)




def main():


    json_file = ''
    url, token = get_url_and_token()
    max_duration = 120
    ## user defined params

    obj = [ "wordcount_20.json" , "wordcount_80.json" ]
    popularity_factor = 80
    #resp_list = []
    global resp_list
    manifest_dir = "manifest"
    thread_list = []

    # usage : python automate_job.py <interval> <no_of_sessions> <popularity_factor>
    if len(sys.argv) == 4:
        interval = int(sys.argv[1])
        no_of_sessions = int(sys.argv[2])
        popularity_factor = int(sys.argv[3])

        for i in range(0, no_of_sessions):

            # pick the random number and match agains popularity factor
            x =  random.randrange(0,99)
            if x<= popularity_factor:
                json_file = get_object(url, token, manifest_dir, obj[0])
            else:
                json_file = get_object(url, token, manifest_dir, obj[1])

            #execute the job
            # create a thread and execute the job
            t_worker = threading.Thread(target=worker, args=( url, token, json_file, i))
            t_worker.start()
            thread_list.append(t_worker)
            #
            #resp = zebra_execute(url, token, json_file)
            #resp_list.append(resp)
            time.sleep(interval)


    # for running the debug run
    elif len(sys.argv) == 1:
        manifest_dir = "debug"
        json_file = get_object(url, token, manifest_dir , obj[0])
        resp = zebra_execute(url, token, json_file)
        resp_list.append(resp)

    else:
        usage()


    # for t in thread_list:
    #     t.join()
    signal = True

    while(signal):
        for t in thread_list:
            if not t.isAlive():
                signal = False

        time.sleep(20)

    jobcounter = 1
    for item in resp_list:
            #     #print_resp (item,jobcounter)
            #     #json_print(item, jobcounter)
        print_report(item, jobcounter)
        jobcounter += 1

if __name__ == '__main__':
    main()

