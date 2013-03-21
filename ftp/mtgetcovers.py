#!/usr/bin/env python
# encoding: utf-8

"""
Created by Liza Daly on Fri Oct 19 10:31:18 2012
Copyright (c) 2012 Safari Books Online. All rights reserved.

Audit the files available on the BvD datastore

"""

import csv
from cStringIO import StringIO
import datetime
import ftplib
import logging
import os.path
import re
import sys
import threading
import Queue, time

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

DATASTORE = 'ftp.bvdep.com'
DATASTORE_USERNAME = 'safaridatastore'
DATASTORE_PASSWORD = '91Jt683a'


OUTFILE_NAME = os.path.join('covers', 'datastore_cover_audit.csv')
outfile = csv.writer(open(OUTFILE_NAME, 'a'))

SKIPFILES = 'skipcoverids.txt'
KNOWN_SKIPFILES = set()

if os.path.exists(SKIPFILES):
    for line in open(SKIPFILES, 'r'):
        KNOWN_SKIPFILES.add(line.strip())

# Set this up for appending
skipfile_names = open(SKIPFILES, 'a', 0) # write the skipfiles unbuffered


def find_ebooks(dirname,trdname):
    conn = ftplib.FTP(DATASTORE, DATASTORE_USERNAME, DATASTORE_PASSWORD, '', 10)
    conn.set_debuglevel(1)
    ftp_list = []
    conn.retrlines('LIST %s' % dirname, ftp_list.append)
    found_match = False
    
    file_type = '.jpg'

    file_list = []
    for item in ftp_list:
        filename = item.split(' ')[-1].strip()
        if filename == dirname + '_large' + file_type or filename == dirname + '_lrg' + file_type or filename == dirname + file_type:
            print bcolors.OKBLUE + trdname + bcolors.ENDC + " Got filename " + filename 
            outfile.writerow([filename, dirname])
            file_list.append(filename)
            found_match = True

    try:
        if found_match:
            if dirname + '_large' + file_type in file_list:
                file_name = dirname + '_large' + file_type
            elif dirname + '_lrg' + file_type in file_list:
                file_name = dirname + '_lrg' + file_type
            elif dirname  + file_type in file_list:
                file_name = dirname + file_type

            local_filename = os.path.join('covers', dirname + file_type)
            print bcolors.OKBLUE + trdname + bcolors.ENDC + " Saving " + file_name + " as " + local_filename
            with open(local_filename, 'w') as f:
                conn.retrbinary('RETR ' + dirname + '/' +  file_name, lambda data: f.write(data))
            f.close()

        if not found_match:
            print bcolors.OKBLUE + trdname + bcolors.ENDC + " Didn't find a " + file_type + " for " + dirname
        skipfile_names.write(dirname + "\n")
        conn.close()
    except:
        conn.close()
        print bcolors.FAIL + trdname + bcolors.ENDC + " Transfer Failed " + file_name

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Starting " + self.name
        process_data(self.name,self.q)
        print "Exiting " + self.name

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            dirname = q.get()
            queueLock.release()

            if dirname not in KNOWN_SKIPFILES:
                print bcolors.OKBLUE + threadName + bcolors.ENDC + " Processing " + dirname
                find_ebooks(dirname,threadName)
            else:
                print bcolors.OKGREEN + threadName + bcolors.ENDC + " Skipping " + dirname

        else:
            queueLock.release()
        #time.sleep(1)

if __name__ == '__main__':
    #threadList = ["Thread-1"]
    threadList = ["Thread-1", "Thread-2","Thread-3", "Thread-4"]
    queueLock = threading.Lock()
    workQueue = Queue.Queue()
    threads = []
    threadID = 1

    # Create new threads
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    queueLock.acquire()
    for listing in open('fpidcover.list'):
        dirname = listing.rstrip()
        workQueue.put(dirname)
    queueLock.release()
            
    # Wait for queue to empty
    while not workQueue.empty():
        the_time = time.time()
        if the_time%10 <= 0.00001:
            print bcolors.FAIL + str(time.ctime(the_time)) + " " + str(threading.active_count() - 1) + " Threads still alive." + bcolors.ENDC
            if threading.active_count() < 5 :
                thread_list = threads[:]
                for thread in thread_list:
                    if not thread.is_alive():
                        threadID = thread.ident
                        tName = thread.name
                        threads.remove(thread)
                        thread = myThread(threadID, tName, workQueue)
                        thread.start()
                        threads.append(thread)
                print bcolors.FAIL + str(time.ctime(time.time())) + " " + str(threading.active_count() - 1) + " Threads still alive." + bcolors.ENDC
        pass

    # Notify threads it's time to exit
    exitFlag = 1

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print "Exiting Main Thread"
