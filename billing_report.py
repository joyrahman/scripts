# __author__ = 'joy'
import csv
import time
import os
from tabulate import tabulate
def print_report(report):
    print tabulate(report, headers=["ID","Status", "Time", "Attrib"])
    #for item in report:
    #    print item

def write_to_csv(csv_data):

    directory_name = "/home/cloudsys/report"
    time_format = '%Y%m%d_%H%M%S'
    current_time = time.strftime(time_format)
    file_extension = "csv"

    output_file_name = "exec_report_{}.{}".format(current_time, file_extension)
    target_path = os.path.join(directory_name,output_file_name)
    with open(target_path, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(csv_data)

def get_billing_report(xNexeSystem, xNexeStatus,  xNexeCdrLine):
    report = []
    totalServerTime, nodesBillingInfo = xNexeCdrLine.split(',', 1)

    xNexeSystem = xNexeSystem.split(',')
    #xNexeError  = xNexeError.split(',')
    xNexeStatus = xNexeStatus.split(',')
    nodesBillingInfo = nodesBillingInfo.split(',')

    i = 0
    for j in xrange(0,len(nodesBillingInfo)-1, 2):
        '''
        record = {}
        record['id'] = xNexeSystem[i]
        #record['session_error'] = xNexeError[i]
        record['status'] = xNexeStatus[i]
        record['time'] = nodesBillingInfo[j]
        record['attrib'] = nodesBillingInfo[j+1]
        '''
        record = [ xNexeSystem[i], xNexeStatus[i], nodesBillingInfo[j], nodesBillingInfo[j+1] ]

        i += 1
        report.append(record)

    print "Total Exec Time: {}".format(totalServerTime)
    print_report(report)
    #write_to_csv(report)

    #return report







def main():
    billing_string = "4.251, 3.994, 0.11 3.53 1262 75929984 34 199 0 0 0 0, \
    4.44, 5.22 1.55 1567 55928884 76 233 0 0 0 0, \
    6.251, 0.11 3.53 1262 75929984 34 199 0 0 0 0, \
    7.251, 0.11 3.53 1262 75929984 34 199 0 0 0 0"

    system_name = "map-1,map-2,map-3,reduce-1,reduce-2"
    system_status = "ok,ok,ok,ok,ZeroVM did not run"
    report = get_billing_report(system_name, system_status, billing_string)
    for item in report:
        print item, "\n"

if __name__ == '__main__':
    main()
