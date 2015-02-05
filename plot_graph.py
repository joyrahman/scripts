import numpy as np
import csv
import matplotlib.pyplot as plt
import sys



def main(file_name, target_container_id):

    target_container_id = target_container_id.split(',')
    fig = plt.figure(figsize=(12, 6))
    hax = fig.add_subplot(122)

    with open(file_name, 'rU') as f:
        print "opening {}".format(file_name)
        reader = csv.reader(f)
        data = list(list(rec) for rec in csv.reader(f, delimiter=','))
        #print data

    for item in data:
        print (item)
        start_time = item[0].split(" ",1)
        start_hour, start_min, start_sec = map(int,start_time[1].split(':'))
        start = (start_hour*3600 + start_min*60 + start_sec )
        print start

        end_time = item[1].split(" ",1)
        end_hour, end_min, end_sec = map(int, end_time[1].split(':'))
        end = end_hour*3600 + end_min*60 + end_sec
        print "end {}".format(end)
        #end_time = item[1].split(" ")[1]
        #end = end_time.split(':')[0]*3600 + end_time.split(':')[1]*60 + end_time.split(':')[2]

        job_id     = item[2]
        container_id = item[3]
        execution_time = item[4]
        for item in target_container_id:
            if container_id == item:
                hax.hlines(int(job_id), start, end, colors = 'red')
            else:
                hax.hlines(int(job_id), start, end, colors = 'blue')

    hax.set_xlabel('time (s)')
    hax.set_xlabel('job_id')
    hax.set_title('Execution Time Impact')
    plt.show()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])


