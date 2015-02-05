import numpy as np
import csv
import matplotlib.pyplot as plt
import sys



def main(file_name):

    with open(file_name, 'rU') as f:
        print "opening {}".format(file_name)
        reader = csv.reader(f, dialect=csv.excel_tab)
        data = list(reader)
        print data

    for item in data:
        start_time = item[0]
        end_time   = item[1]
        job_id     = item[2]
        container_id = item[3]
        execution_time = item[4]
        plt.hlines(job_id,start_time, end_time, colors = 'red')

    plt.show()


if __name__ == '__main__':
    main(sys.argv[1])

