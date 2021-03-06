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
    output_file_name = "exec_report_{}.{}".format(current_time, file_extension)
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
    output_file_name = "report_{}.{}".format(current_time, file_extension)
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
    t = (start_time,end_time,job_no,manifest_id,totalExecutionTime)
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
    print 'python automated_job2.py {interval} {no_of_sessions} {popularity}'
    sys.exit(1)




def main():


    json_file = ''
    url, token = get_url_and_token()
    max_duration = 120
    ## user defined params

    #obj = [ "wordcount_20.json" , "wordcount_80.json" ]
    obj = [ "wordcount_dir1.json" , \
            "wordcount_dir2.json" , \
            "wordcount_dir3.json" , \
            "wordcount_dir4.json" , \
            "wordcount_dir5.json" , \
            "wordcount_dir6.json" , \
            "wordcount_dir7.json" , \
            "wordcount_dir8.json" , \
            "wordcount_dir9.json" , \
            "wordcount_dir10.json" ]

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
        z = 0
        manifest_id = -1
        for i in range(0, no_of_sessions):

            # pick the random number and match agains popularity factor
            x =  random.randrange(0,99,2)
            #print x
            if popularity_factor == 50:
                p = z%2
                json_file = get_object(url, token, manifest_dir, obj[p])
                manifest_id = p
                print "manifest of job: ",p,"\n\n"
                print json_file
                z += 1

            elif popularity_factor == -1:
                # run unbiased execution
                p = random.randrange(0,10)
                #print "manifest:{} job_id:{}".format(p,i)
                manifest_id = p
                json_file = get_object(url,token, manifest_dir, obj[p])

            elif popularity_factor == -2:
                # run specific job for a single fine
                json_file = get_object(url, token, manifest_dir, "wordcount_file1.json")
                manifest_id = 11

            elif x<= popularity_factor:
                p = random.randrange(0,2,1)
                json_file = get_object(url, token, manifest_dir, obj[p])
                manifest_id = p
            else:
                p = random.randrange(3,10,1)
                json_file = get_object(url, token, manifest_dir, obj[p])
                manifest_id = p

            #execute the job
            # create a thread and execute the job

            t_worker = threading.Thread(target=worker, args=( url, token, json_file, i, manifest_id ))
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
    # signal = True
    #
    # while(signal):

    ### BUSY WAIT UNTIL ALL THREADS ARE DEAD ###
    signal = True
    signal_flag = [0] * len(thread_list)

    while signal:
        i = 0
        for t in thread_list:
            if t.isAlive():
                signal_flag[i] = 1
            else :
                signal_flag[i] = 0
            i += 1

        sum = 0
        for item in signal_flag:
            sum += item

        if sum ==0:
            signal = False
        else:
            time.sleep(5)


    global record
    #global csv_data
    ## write the data to db and csv
    write_to_db(record)
    write_to_csv(record)


if __name__ == '__main__':
    main()

