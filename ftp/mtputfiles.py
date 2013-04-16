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
import re
import sys
import threading, Queue, time
import os, filecmp, shutil

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

DATASTORE = 'cowbird.seb.safaribooks.com'
DATASTORE_USERNAME = 'sboassets'
DATASTORE_PASSWORD = 'TRud4Ubr'

OUTFILE_NAME = os.path.join('out', 'datastore_audit.csv')
outfile = csv.writer(open(OUTFILE_NAME, 'a'))

SKIPFILES = 'skipfiles.txt'
KNOWN_SKIPFILES = set()

if os.path.exists(SKIPFILES):
    for line in open(SKIPFILES, 'r'):
        KNOWN_SKIPFILES.add(line.strip())

# Set this up for appending
skipfile_names = open(SKIPFILES, 'a', 0) # write the skipfiles unbuffered


def deposit_ebooks(filename,trdname):
    conn = ftplib.FTP(DATASTORE, DATASTORE_USERNAME, DATASTORE_PASSWORD, '', 10)
    conn.set_debuglevel(1)

    conn.cwd('large')

    try:
        if os.path.exists(filename):
            fname = os.path.split(filename)[1]
            print bcolors.OKBLUE + trdname + bcolors.ENDC + " Uploading " + filename + " as " + fname 
            conn.storbinary('STOR ' + fname, open(filename, 'r'))
        else:
            print bcolors.FAIL + trdname + bcolors.ENDC + " File " + filename + " does not exists!"
        skipfile_names.write(filename + "\n")
        conn.close()
    except:
        print bcolors.FAIL + trdname + bcolors.ENDC + " Transfer Failed " + file_name
        conn.close()

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
            filename = q.get()
            queueLock.release()

            if filename not in KNOWN_SKIPFILES:
                print bcolors.OKBLUE + threadName + bcolors.ENDC + " Processing " + filename
                deposit_ebooks(filename,threadName)
            else:
                print bcolors.OKGREEN + threadName + bcolors.ENDC + " Skipping " + filename

        else:
            queueLock.release()
        #time.sleep(1)


def get_file_list():
    BASE_DIR = "/home/content/uploaded/Cowbird"

    file_list = []
    for dirpath, dirnames, filenames in os.walk(BASE_DIR):
        for files in filenames:
            file_list.append(os.path.join(dirpath,files))
    return file_list


if __name__ == '__main__':
    threadList = ["Thread-1", "Thread-2"]
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
    for listing in get_file_list():
        filename = listing.rstrip()
        workQueue.put(filename)
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
