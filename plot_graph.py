import numpy as np
import csv
import matplotlib.pyplot as plt
import sys


def draw_multigraph(file_name1, file_name2, target_container_id):
    target_container_id = target_container_id.split(',')
    fig = plt.figure(figsize=(12, 6))
    vax = fig.add_subplot(121)
    hax = fig.add_subplot(122)
    draw_plot(file_name1,target_container_id,vax)
    draw_plot(file_name2,target_container_id,hax)
    plt.show()


def draw_singlegraph(file_name, target_container_id):
    target_container_id = target_container_id.split(',')
    fig = plt.figure(figsize=(12, 6))
    hax = fig.add_subplot(122)
    draw_plot(file_name, target_container_id, hax)
    plt.show()

def draw_plot(file_name, target_container_id, plot_obj):


#def main(file_name, target_container_id):

 #   target_container_id = target_container_id.split(',')
 #   fig = plt.figure(figsize=(12, 6))
 #   hax = fig.add_subplot(122)
    hax = plot_obj
    print target_container_id
    with open(file_name, 'rU') as f:
        print "opening {}".format(file_name)
        reader = csv.reader(f)
        data = list(list(rec) for rec in csv.reader(f, delimiter=','))
        #print data

    for item in data:
        #print (item)
        start_time = item[0].split(" ",1)
        start_hour, start_min, start_sec = map(int,start_time[1].split(':'))
        start = (start_hour*3600 + start_min*60 + start_sec )
        #print start

        end_time = item[1].split(" ",1)
        end_hour, end_min, end_sec = map(int, end_time[1].split(':'))
        end = end_hour*3600 + end_min*60 + end_sec
        #print "end {}".format(end)
        #end_time = item[1].split(" ")[1]
        #end = end_time.split(':')[0]*3600 + end_time.split(':')[1]*60 + end_time.split(':')[2]

        job_id     = item[2]
        container_id = item[3]
        print container_id
        execution_time = item[4]
        #for item in target_container_id:
        if container_id in target_container_id:
            hax.hlines(int(job_id), start, end, colors = 'red')
        else:
            hax.hlines(int(job_id), start, end, colors = 'blue')

    hax.set_xlabel('horizontal line = start_time, end_time')
    hax.set_ylabel('job_id')
    hax.set_title('Exec Time')
    #hax.set_title('Job Arrival Rate:{} Popularity Factor:{} Container_ID:{}'.format('1','True','0,1'))


def usage():
    print "file_name1 file_name2 container_list<'01'> "


if __name__ == '__main__':
    if len(sys.argv)==3:
        draw_singlegraph(sys.argv[1], sys.argv[2])
    elif len(sys.argv)==4:
        draw_multigraph(sys.argv[1], sys.argv[2],sys.argv[3])
    else:
        usage()


