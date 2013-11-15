#!/usr/bin/env python
# encoding: utf-8

"""
Created by Matthew Hare on March 25th, 2013
Copyright (c) 2012 Safari Books Online. All rights reserved.

Crawl over the Datastore for dates, awwwyeah!

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

RETIREDFILE = 'retired_fpids.skip'
SKIPFILE = 'datastore_date_audit.skip'
KNOWN_SKIPFILES = set()

if os.path.exists(RETIREDFILE):
    for line in open(RETIREDFILE, 'r'):
        KNOWN_SKIPFILES.add(line.strip())

OUTFILE_NAME = 'datastore_date_audit.csv'
outfile = csv.writer(open(OUTFILE_NAME, 'a'))

the_end = False

def parse_file_name(item):
    fn_list = [x for x in item.split(' ') if x != ''][8:]
    fn = ''
    for item in fn_list:
        fn = fn + item + ' '
    fn = fn.strip()
    return fn

def date_crawler():
    if os.path.exists(SKIPFILE):
        for line in open(SKIPFILE, 'r'):
            KNOWN_SKIPFILES.add(line.strip())

    # Set this up for appending
    skipfile_names = open(SKIPFILE, 'a', 0) # write the skipfiles unbuffered

    conn = ftplib.FTP(DATASTORE, DATASTORE_USERNAME, DATASTORE_PASSWORD, '', 20)
    conn.set_debuglevel(0)
    ftp_list = []
    try:
        conn.retrlines('LIST .', ftp_list.append)
    except:
        print "got exception 1 "
        return

    dir_list = []
    for item in ftp_list:
        if item[0] == 'd':
            folder = item.split(' ')[-1]
            if folder[0] != '.' and folder[0] != "'" and folder[0] != '_' and 'coursesmart' not in folder.lower() and folder not in KNOWN_SKIPFILES:
                dir_list.append(folder)

    for dirrectory in dir_list:
        newest_edate = None
        newest_pdate = None
        content_list = []
        folder_list = []
        try:
            conn.retrlines('LIST {}'.format(dirrectory), content_list.append)
        except:
            print "got exception 2 " + dirrectory
            return
        for item in content_list:
            if item[0] == 'd':
                folder = item.split(' ')[-1]
                if folder[0] != '.' and folder[0] != "'" and folder[0] != '_':
                    folder_list.append(folder)
            elif item[0] == '-' and item.endswith('.epub'):
                file_name = parse_file_name(item)
                try:
                    modified_time = conn.sendcmd('MDTM {}/{}'.format(dirrectory,file_name)).split(' ')[-1]
                except:
                    print "got exception 3 " + dirrectory + "/" + file_name
                    return
                if modified_time > newest_edate:
                    newest_edate = modified_time
            elif item[0] == '-' and item.endswith('.pdf'):
                file_name = parse_file_name(item)
                try:
                    modified_time = conn.sendcmd('MDTM {}/{}'.format(dirrectory,file_name)).split(' ')[-1]
                except:
                    print "got exception 4 " + dirrectory + "/" + file_name
                    return
                if modified_time > newest_pdate:
                    newest_pdate = modified_time
                
        for folder in folder_list:
            content_list = []
            try:
                conn.retrlines('LIST {}/{}'.format(dirrectory,folder), content_list.append)
            except:
                print "got exception 5 " + dirrectory + "/" + folder
                return
            for item in content_list:
                if item[0] == '-' and item.endswith('.epub'):
                    file_name = parse_file_name(item)
                    try:
                        modified_time = conn.sendcmd('MDTM {}/{}/{}'.format(dirrectory,folder,file_name)).split(' ')[-1]
                    except:
                        print "got exception 6 " + dirrectory + "/" + folder + "/" + file_name
                        return
                    if modified_time > newest_edate:
                        newest_edate = modified_time
                elif item[0] == '-' and item.endswith('.pdf') and folder == 'singlepdf':
                    file_name = parse_file_name(item)
                    try:
                        modified_time = conn.sendcmd('MDTM {}/{}/{}'.format(dirrectory,folder,file_name)).split(' ')[-1]
                    except:
                        print "got exception 7" + dirrectory + "/" + folder + "/" + file_name
                        return
                    if modified_time > newest_pdate:
                        newest_pdate = modified_time


        if newest_edate != None:
            edate = '{}-{}-{}T{}:{}z'.format(newest_edate[0:4],newest_edate[4:6],newest_edate[6:8],newest_edate[8:10],newest_edate[10:12])
        else:
            edate = 'None'
        if newest_pdate != None:
            pdate = '{}-{}-{}T{}:{}z'.format(newest_pdate[0:4],newest_pdate[4:6],newest_pdate[6:8],newest_pdate[8:10],newest_pdate[10:12])
        else:
            pdate = 'None'
        print "{},{},{}".format(dirrectory,edate,pdate)
        outfile.writerow([dirrectory,edate,pdate])
        skipfile_names.write(dirrectory + "\n")
    the_end = True

if __name__ == '__main__':
    while not the_end:
        date_crawler()
