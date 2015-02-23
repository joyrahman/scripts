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

def write_to_csv(csv_data):
    directory_name = "/home/cloudsys/report"
    time_format = '%Y-%m-%d %H:%M:%S'
    current_time = time.strftime(time_format)
    file_extension = "csv"
    output_file_name = "file_size_report_{}.{}".format(current_time, file_extension)
    print("[>>] writing to csv file: {}".format(output_file_name))
    target_path = os.path.join(directory_name,output_file_name)
    with open(target_path, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(csv_data)

def write_to_db(data):
    directory_name = "/home/cloudsys/report"
    time_format = '%Y-%m-%d %H:%M:%S'
    current_time = time.strftime(time_format)
    file_extension = "db"
    output_file_name = "file_size_report_{}.{}".format(current_time, file_extension)
    target_path = os.path.join(directory_name,output_file_name)
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

def execute_job(url, token, json_file, job_id, manifest_id):
    global resp_list
    #logging.debug("running the job")
    time_format = '%Y-%m-%d %H:%M:%S'
    start_time = time.strftime(time_format)

    try:
        resp = zebra_execute(url,token,json_file)
        end_time = time.strftime(time_format)
        populate_record(resp,start_time,end_time,job_id,manifest_id)

    except Exception as Inst:
        #logging.debug ("Got some Error as worker>>",Inst)
        print Inst






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



def populate_record(resp, start_time, end_time, job_no='',manifest_id=0):
    global record
    global csv_data
    totalExecutionTime, nodesBillingInfo = resp.headers['x-nexe-cdr-line'].split(',', 1)
    print ("{}, {}, {}, {}, {}").format(start_time, end_time, job_no, manifest_id, float(totalExecutionTime))
    t = (start_time,end_time,job_no,manifest_id,totalExecutionTime)
    record.append(t)
    #csv_data.append([start_time,end_time,job_no,manifest_id,totalExecutionTime])





def usage():
    #print 'automate_script.py <container_name> <json_name> <interval> <no_of_sessions>'
    print 'python automated_job2.py {interval} {no_of_sessions} {popularity}'
    sys.exit(1)




def main():


    json_file = ''
    url, token = get_url_and_token()
    obj = [ "wordcount_dir_35mb.json" , \
            "wordcount_dir_180mb.json"  ]
    interval = 60

    global resp_list
    manifest_dir = "manifest"
    k = 0
    for file_name in obj:
        json_file = get_object(url, token, manifest_dir, file_name)
        execute_job(url, token, json_file, k, k)
        k += 1
        time.sleep(interval)
    global record
    write_to_db(record)
    write_to_csv(record)


if __name__ == '__main__':
    main()

