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
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

    def disable(self):
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.ENDC = ''


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

DATASTORE = 'ftp.bvdep.com'
DATASTORE_USERNAME = 'safaridatastore'
DATASTORE_PASSWORD = '91Jt683a'

bvdlog = open('bvdquery.log', 'w') 

OUTFILE_NAME = os.path.join('out', 'datastore_audit.csv')
outfile = csv.writer(open(OUTFILE_NAME, 'a'))

SKIPFILES = 'bvdquery.skip'
KNOWN_SKIPFILES = set()

if os.path.exists(SKIPFILES):
    for line in open(SKIPFILES, 'r'):
        KNOWN_SKIPFILES.add(line.strip())

# Set this up for appending
skipfile_names = open(SKIPFILES, 'a', 0) # write the skipfiles unbuffered


def find_ebooks(dirname,trdname):
    conn = ftplib.FTP(DATASTORE, DATASTORE_USERNAME, DATASTORE_PASSWORD, '', 10)
    conn.set_debuglevel(0)
    ftp_list = []
    conn.retrlines('LIST %s' % dirname, ftp_list.append)
    found_match = False

    file_list = []
    if len(ftp_list) == 0: bvdlog.write("{} not found \n".format(dirname))
    for item in ftp_list:
        bvdlog.write(item + "\n")

    skipfile_names.write(dirname + "\n")
    conn.close()

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        bvdlog.write("Starting " + self.name + "\n")
        process_data(self.name,self.q)
        bvdlog.write("Exiting " + self.name + "\n")

def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            dirname = q.get()
            queueLock.release()

            if dirname not in KNOWN_SKIPFILES:
                
                bvdlog.write(bcolors.OKBLUE + "======================================================" + bcolors.ENDC + "\n")
                bvdlog.write(bcolors.OKBLUE + threadName + bcolors.ENDC + " Processing " + dirname + "\n")
                find_ebooks(dirname,threadName)
            else:
                bvdlog.write(bcolors.OKGREEN + threadName + bcolors.ENDC + " Skipping " + dirname + "\n")

        else:
            queueLock.release()
        #time.sleep(1)




if __name__ == '__main__':
    threadList = ["Thread-1"]
    #threadList = ["Thread-1", "Thread-2"]
    #threadList = ["Thread-1", "Thread-2","Thread-3", "Thread-4"]
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
    for listing in open('fpid.list'):
        dirname = listing.rstrip()
        workQueue.put(dirname)
    queueLock.release()
            
    # Wait for queue to empty
    while not workQueue.empty():
        the_time = time.time()
        if the_time%10 <= 0.00001:
            bvdlog.write(bcolors.FAIL + str(time.ctime(the_time)) + " " + str(threading.active_count() - 1) + " Threads still alive." + bcolors.ENDC + "\n")
            if threading.active_count() < 2 :
                thread_list = threads[:]
                for thread in thread_list:
                    if not thread.is_alive():
                        threadID = thread.ident
                        tName = thread.name
                        threads.remove(thread)
                        thread = myThread(threadID, tName, workQueue)
                        thread.start()
                        threads.append(thread)
                bvdlog.write(bcolors.FAIL + str(time.ctime(time.time())) + " " + str(threading.active_count() - 1) + " Threads still alive." + bcolors.ENDC + "")
        pass

    # Notify threads it's time to exit
    exitFlag = 1

    # Wait for all threads to complete
    for t in threads:
        t.join()
    bvdlog.write("Exiting Main Thread \n")
