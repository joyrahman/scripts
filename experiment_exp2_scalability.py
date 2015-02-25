# new branch
#!/usr/bin/env python

#new change
import billing_report
import requests
import json
import sys
import os
import random
import time
import datetime
import threading
import sqlite3 as lite
import csv


con = None
resp_list = []
record = []
#csv_data = []

def write_to_csv(csv_data, output_file_name):
    directory_name = "/home/cloudsys/report"
    time_format = '%Y-%m-%d %H:%M:%S'
    current_time = time.strftime(time_format)
    file_extension = ".csv"
    if not output_file_name:
        output_file_name = "exec_report_{}".format(current_time)
    print("[>>] writing to csv file: {}".format(output_file_name))
    output_file_name = output_file_name + file_extension
    target_path = os.path.join(directory_name, output_file_name)
    with open(target_path, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(csv_data)

def write_to_db(data, output_file_name):
    directory_name = "/home/cloudsys/report"
    time_format = '%Y-%m-%d %H:%M:%S'
    current_time = time.strftime(time_format)
    file_extension = ".db"
    if not output_file_name:
        output_file_name = "report_{}".format(current_time)
    target_path = os.path.join(directory_name,output_file_name+file_extension)
    con = lite.connect(target_path)
    print("[>>] writing to db")
    with con:
         cur = con.cursor()
         cur.execute("DROP TABLE IF EXISTS CDR")
         cur.execute("CREATE TABLE CDR(start_time DATE, end_time DATE, job_id INT, container_id INT, execution_time DOUBLE )")
         for item in data:
            cur.execute("INSERT INTO CDR VALUES(?,?,?,?,?)",item)




#import logging

#logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)


def worker(url, token, json_file, job_id, manifest_id=0):
    global resp_list
    #logging.debug("running the job")
    time_format = '%Y-%m-%d %H:%M:%S'
    start_time = time.strftime(time_format)

    try:
        resp = zebra_execute(url,token,json_file)
        #print resp
        #print_report(resp,start_time, job_id, manifest_id )
        end_time = time.strftime(time_format)
        populate_record(resp,start_time,end_time,job_id,manifest_id)
        #json_print(resp, job_id)
        #resp_list.append(resp)
        #print_report(resp)
    except Exception as Inst:
        #logging.debug ("Got some Error as worker>>",Inst)
        print Inst
    #finally:
     #   print_report(resp)
        #print_resp(resp,job_id)




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

def populate_record(resp, start_time, end_time, job_no='',manifest_id=0):
    global record
    global csv_data
    totalExecutionTime, nodesBillingInfo = resp.headers['x-nexe-cdr-line'].split(',', 1)
    print ("{}, {}, {}, {}, {}").format(start_time, end_time, job_no, manifest_id, float(totalExecutionTime))
    #t = (start_time,end_time,job_no,manifest_id,totalExecutionTime)
    t = (job_no,totalExecutionTime)
    record.append(t)
    #csv_data.append([start_time,end_time,job_no,manifest_id,totalExecutionTime])



def print_report(resp, start_time, job_no='',manifest_id=0 ):
    #x-nexe-system
    #x-nexe-error
    #x-nexe-cdr-line
    #x-nexe-status
    #print resp.__dict__
    #print("-------Job:",job_no,"---------")

    end_time = time.time()

    totalExecutionTime, nodesBillingInfo = resp.headers['x-nexe-cdr-line'].split(',', 1)
    print ("{}, {}, {}, {}, {}").format(start_time, end_time, job_no, manifest_id, totalExecutionTime)
    sessions_id     = resp.headers['x-nexe-system']
    sessions_error  = " "
    if 'x-nexe-error' in resp.headers:
        sessions_error  = resp.headers['x-nexe-error']
    sessions_status = resp.headers['x-nexe-status']
    sessions_cdr    = resp.headers['x-nexe-cdr-line']
    #billing_report.get_billing_report(sessions_id, sessions_error, sessions_status, sessions_cdr)

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
    print 'python automate_job.py <interval> <no_of_sessions> <popularity_factor> <manifest_dir> <manifest_file_name> <output_file>'
    sys.exit(1)




def main():


    json_file = ''
    url, token = get_url_and_token()
    max_duration = 120

    global resp_list

    # usage : python automate_job.py <interval> <no_of_sessions> <popularity_factor> <manifest_dir><output_file>
    if len(sys.argv) >= 5:

        interval = int(sys.argv[1])
        no_of_sessions = int(sys.argv[2])
        popularity_factor = int(sys.argv[3])
        output_file_name = sys.argv[6]
        manifest_dir = sys.argv[4]
        manifest_file = sys.argv[5]
        json_file = get_object(url,token, manifest_dir, manifest_file)
        time_format = '%Y-%m-%d %H:%M:%S'
        start_time = time.strftime(time_format)
        resp = zebra_execute(url, token, json_file)
        end_time = time.strftime(time_format)
        job_id = 1
        populate_record(resp,start_time,end_time)
        resp_list.append(resp)
        global record
        write_to_csv(record,output_file_name)



    # for running the debug run

    else:
        usage()



if __name__ == '__main__':
    main()

