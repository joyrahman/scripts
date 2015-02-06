import urllib2
import requests
import sys
import os, tempfile
import json
import subprocess
import time
import logging


'''
python swift_download.py [source_container] [dest_container]
'''

def set_logging():
    # logging configuration
    logger = logging.getLogger('swift downloader')
    logger.setLevel(logging.DEBUG)


    # create file handler which logs even debug messages
    fh = logging.FileHandler('time.log')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger



def main(src_container, dst_container ):

    # logging configuration
    logger = logging.getLogger('swift downloader')
    logger.setLevel(logging.DEBUG)


    # create file handler which logs even debug messages
    fh = logging.FileHandler('time.log')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)



    logger.info('swift download started')
    container_url= os.environ['OS_STORAGE_URL'] + "/" + src_container

    auth_token = os.environ['OS_AUTH_TOKEN']
    header_parameters = { 'X-Auth-Token': '{}'.format(auth_token)}


    # Connect to the Swift Server
    directory_list = requests.get( container_url,  headers = header_parameters)
    listing = str(directory_list.text).split("\n")
    listing =  filter(None, listing)
    i = 0

    # command_str = 'mkdir {}'.format(dst_container)
    # p = subprocess.Popen( command_str , shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # for line in p.stdout.readlines():
    #     print line
    # retval = p.wait()
    # print retval


    if not os.path.isdir(dst_container):
        os.mkdir(dst_container)


    for item in listing:
        i += 1
        request_string = urllib2.Request(container_url + "/"+item, headers=header_parameters)
        remote_fp =  urllib2.urlopen(request_string)
        output = open(os.path.join(dst_container,item), 'wb')
        output.write(remote_fp.read())
        output.close()

    logger.info('*** copy done ***')


def usage():
    print 'python swift_download.py [src_container] [dst_container]'

if __name__ == '__main__':
    if len(sys.argv) == 3:
        src_container = sys.argv[1]
        dst_container = sys.argv[2]
        main(src_container, dst_container)
    else:
        usage()
