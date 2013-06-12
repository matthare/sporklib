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
from datetime import date
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

RETIREDFILE = 'retired_fpid.skip'
SKIPFILE = 'datastore_date.skip'
KNOWN_SKIPFILES = set()

if os.path.exists(RETIREDFILE):
    for line in open(RETIREDFILE, 'r'):
        KNOWN_SKIPFILES.add(line.strip())

the_end = False

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
    except Exception:
        print "got exception 1 "
        return

    dir_list = []
    for item in ftp_list:
        if item[0] == 'd':
            folder = item.split(' ')[-1]
            if folder[0] != '.' and folder[0] != "'" and folder[0] != '_' and 'coursesmart' not in folder.lower() and folder not in KNOWN_SKIPFILES:
                dir_list.append(folder)

    print "{} folders".format(len(dir_list))
    for dirrectory in dir_list:
        content_list = []
        try:
            conn.retrlines('LIST {}'.format(dirrectory), content_list.append)
        except Exception:
            print "got exception 2 " + dirrectory
            return
        for item in content_list:
            if item[0] == '-' and item.endswith('backup.epub'):
                year = item.split()[len(item.split()) - 2]
                day = item.split()[len(item.split()) - 3]
                month = item.split()[len(item.split()) - 4]
                goodyear = False
                try:
                    year = int(year)
                    if year >= 2013:
                        goodyear = True
                except Exception:
                    if ":" in year:
                        goodyear = True
                    else:
                        print item.split()
                        continue

                if goodyear and month is not 'Jan':
                    print dirrectory

        skipfile_names.write(dirrectory + "\n")
    the_end = True

if __name__ == '__main__':
    while not the_end:
        date_crawler()
