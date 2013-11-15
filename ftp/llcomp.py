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
import os
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

BASE_DIR = "/mnt/llnw_video"
ignore_dirs = []

# Credentials
LLNW_HOST = 'safxcode.upload.llnw.net'
LLNW_USERNAME = 'safxcode-ht'
LLNW_PASSWORD = 'vm54ep'

RETIREDFILE = 'retired_fpids.skip'
SKIPFILE = 'datastore_date_audit.skip'
KNOWN_SKIPFILES = set()

if os.path.exists(RETIREDFILE):
    for line in open(RETIREDFILE, 'r'):
        KNOWN_SKIPFILES.add(line.strip())

OUTFILE_NAME = 'datastore_date_audit.csv'
outfile = csv.writer(open(OUTFILE_NAME, 'a'))

def parse_file_name(item):
    fn_list = [x for x in item.split(' ') if x != ''][8:]
    fn = ''
    for item in fn_list:
        fn = fn + item + ' '
    fn = fn.strip()
    return fn

def parse_file_year(item):
    fn_list = [x for x in item.split(' ') if x != ''][7:8]
    fn = ''
    for item in fn_list:
        fn = fn + item + ' '
    fn = fn.strip()
    return fn

def parse_file_month(item):
    fn_list = [x for x in item.split(' ') if x != ''][5:6]
    fn = ''
    for item in fn_list:
        fn = fn + item + ' '
    fn = fn.strip()
    return fn

def ll_comp():
    
    local_dir_list = []
    for dirpath, dirnames, filenames in os.walk(BASE_DIR):
        if dirpath is BASE_DIR:
            local_dir_list = dirnames

    llnw_conn = ftplib.FTP(LLNW_HOST)
    llnw_conn.login(LLNW_USERNAME, LLNW_PASSWORD)

    llnw_conn.cwd('/s/_hold')

    ftp_list = []
    llnw_conn.retrlines('LIST /s/_hold', ftp_list.append)
    llnw_conn.close()

    remote_dir_list = [parse_file_name(item) for item in ftp_list]

    diff_set =  set(remote_dir_list) - set(local_dir_list)
    
    print "----------------------------"
    for item in diff_set:
        print item
    print "----------------------------"


    for item in ftp_list:
        if '2013' in parse_file_year(item) or ':' in parse_file_year(item):
            if 'Apr' in parse_file_month(item) or 'May' in parse_file_month(item) or 'Jun' in parse_file_month(item):
                if parse_file_name(item) not in diff_set:
                    print parse_file_name(item)

    for fpid in diff_set:
        print fpid


if __name__ == '__main__':
    ll_comp()
