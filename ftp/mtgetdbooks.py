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
import zipfile
import shutil

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


OUTFILE_NAME = os.path.join('dbooks', 'datastore_audit.csv')
outfile = csv.writer(open(OUTFILE_NAME, 'a'))

SKIPFILES = 'mtgetdbooks.skip'
KNOWN_SKIPFILES = set()

if os.path.exists(SKIPFILES):
    for line in open(SKIPFILES, 'r'):
        KNOWN_SKIPFILES.add(line.strip())

# Set this up for appending
skipfile_names = open(SKIPFILES, 'a', 0) # write the skipfiles unbuffered


def find_ebooks(dirname,trdname):
    found_match = False

    conn = ftplib.FTP(DATASTORE, DATASTORE_USERNAME, DATASTORE_PASSWORD, '', 10)
    conn.set_debuglevel(0)

    ftp_list = []
    conn.retrlines('LIST {}'.format(dirname), ftp_list.append)

    file_list = []
    dir_list = []
    for item in ftp_list:
        #filename = item.split(' ')[-1].strip()
        filename = ''
        for thing in item.rsplit()[8:]:
            filename = filename + ' ' + thing
        filename = filename.strip()
        if item[0] == 'd' and filename[0] != '.': 
            dir_list.append("{}/{}".format(dirname,filename))
        elif item[0] == '-':
            file_list.append("{}/{}".format(dirname,filename))


    ftp_list_save = []
    ftp_list_save.extend(ftp_list)
    for drctry in dir_list:
        ftp_list = []
        conn.retrlines('LIST {}'.format(drctry), ftp_list.append)

        for item in ftp_list:
            #filename = item.split(' ')[-1].strip()
            filename = ''
            for thing in item.rsplit()[8:]:
                filename = filename + ' ' + thing
            filename = filename.strip()
            if item[0] == 'd' and filename[0] != '.': 
                print "The Rabit Hole goes Deeper Still {}".format(dirname)
            elif item[0] == '-':
                file_list.append("{}/{}".format(drctry,filename))
        ftp_list_save.extend(ftp_list)


    if not os.path.exists(os.path.join('dbooks',dirname)):
        os.makedirs(os.path.join('dbooks',dirname))

    local_file_list = []
    for item in file_list:
        folders = item.split('/')
        if len(folders) == 3:
            if not os.path.exists(os.path.join('dbooks',folders[0],folders[1])):
                os.makedirs(os.path.join('dbooks',folders[0],folders[1]))
        elif len(folders) > 3:
            print "The Rabit Hole deeper Deeper Somehow {}".format(dirname)
            


        local_filename = os.path.join('dbooks', item)

        download_file = True
        my_item = [x for x in ftp_list_save if x.endswith(" {}".format(item.split('/')[-1]))]
        ftp_fsize = int([x for x in my_item[0].split(' ') if x != ''][4])
        if os.path.exists(local_filename):
            fsize = os.path.getsize(local_filename)
            if fsize == ftp_fsize:
                download_file = False
            else:
                download_file = True
                print bcolors.OKBLUE + trdname + bcolors.ENDC + "File exists but differnt size, downloading again: "
                print bcolors.OKBLUE + trdname + bcolors.ENDC + " " + local_filename
                print bcolors.OKBLUE + trdname + bcolors.ENDC + "local size " + str(fsize)
                print bcolors.OKBLUE + trdname + bcolors.ENDC + "remote size " + str(ftp_fsize)
                    


        if download_file:
            print bcolors.OKBLUE + trdname + bcolors.ENDC + " Saving " + item + " as " + local_filename
            with open(local_filename, 'w') as f:
                conn.retrbinary('RETR ' + item, lambda data: f.write(data))
        local_file_list.append(local_filename)

    with zipfile.ZipFile(os.path.join('dbooks','{}.zip'.format(dirname)),'w') as myzip:
        for item in local_file_list:
            file_name = item.strip('dbooks/')
            myzip.write(item,arcname = file_name)

    shutil.rmtree(os.path.join('dbooks',dirname))
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
    for listing in open('fpiddbook.list'):
        dirname = listing.rstrip()
        workQueue.put(dirname)
    queueLock.release()
            
    # Wait for queue to empty
    while not workQueue.empty():
        the_time = time.time()
        if the_time%10 <= 0.00001:
            print bcolors.FAIL + str(time.ctime(the_time)) + " " + str(threading.active_count() - 1) + " Threads still alive." + bcolors.ENDC
            if threading.active_count() < len(threadList) + 1 :
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
