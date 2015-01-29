# __author__ = 'joy'



def billing_report(xNexeCdrLine):
    report = []
    totalServerTime, nodesBillingInfo = xNexeCdrLine.split(',', 1)


    j = 0  #for in in range(0, len(nodesBillingInfo))
    nodesBillingInfo = nodesBillingInfo.split(',')

    for j in xrange(0,len(nodesBillingInfo)-1, 2):
        record = {}
        record['session_time'] = nodesBillingInfo[j]
        record['session_attributes'] = nodesBillingInfo[j+1]
        #print "session_time-{}:{}".format(j, session_time)
        #j += 2
        report.append(record)

    print report


def main():
    test_string = "4.251, 3.994, 0.11 3.53 1262 75929984 34 199 0 0 0 0, 4.44, 0.22 1.55 1567 55928884 76 233 0 0 0 0"
    billing_report(test_string)


if __name__ == '__main__':
    main()
