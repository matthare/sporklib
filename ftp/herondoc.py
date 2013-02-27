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

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

DATASTORE = 'ftp.bvdep.com'
DATASTORE_USERNAME = 'safaridatastore'
DATASTORE_PASSWORD = '91Jt683a'


OUTFILE_NAME = os.path.join('heron', 'datastore_audit.csv')
outfile = csv.writer(open(OUTFILE_NAME, 'a'))

SKIPFILES = 'skipids2.txt'
KNOWN_SKIPFILES = set()

if os.path.exists(SKIPFILES):
    for line in open(SKIPFILES, 'r'):
        KNOWN_SKIPFILES.add(line.strip())

# Set this up for appending
skipfile_names = open(SKIPFILES, 'a', 0) # write the skipfiles unbuffered


def find_ebooks(dirname):
    found_match = True
    conn = ftplib.FTP(DATASTORE, DATASTORE_USERNAME, DATASTORE_PASSWORD, '', 10)
    conn.set_debuglevel(2)
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    conn.retrlines('LIST %s' % dirname)
    sys.stdout = old_stdout

    if not os.path.exists(os.path.join('heron',dirname)):
        os.mkdir(os.path.join('heron',dirname))

    file_list = []
    dir_list = []
    for listing in mystdout.getvalue().split("\n"):
        if listing[:3] == '-rw':
            filename = listing.split(' ')[-1].strip()
            local_filename = os.path.join('heron', dirname, filename)
            log.info("Saving " + filename + " as " + local_filename)
            with open(local_filename, 'w') as f:
                conn.retrbinary('RETR ' + dirname + '/' +  filename, lambda data: f.write(data))
            f.close()

        elif listing[:3] == 'drw':
            subdirname = listing.split(' ')[-1].strip()
            if subdirname[0] != '.':
                dir_list.append(subdirname)

    for directory in dir_list:

        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        conn.retrlines('LIST %s' % os.path.join(dirname,directory))
        sys.stdout = old_stdout
        
        if not os.path.exists(os.path.join('heron',dirname,directory)):
            os.mkdir(os.path.join('heron',dirname,directory))

        for listing in mystdout.getvalue().split("\n"):
            if listing[:3] == '-rw':
                filename = listing.split(' ')[-1].strip()
                local_filename = os.path.join('heron', dirname, directory, filename)
                log.info("Saving " + filename + " as " + local_filename)
                with open(local_filename, 'w') as f:
                    conn.retrbinary('RETR ' + dirname + '/' + directory + "/" + filename, lambda data: f.write(data))
                f.close()
            elif listing[:3] == 'drw':
                subdirname = listing.split(' ')[-1].strip()
                if subdirname[0] != '.':
                    print "Found more subdirs " + subdirname
                        
    if not found_match:
        log.info("Didn't find a PDF or an EPUB for %s" % dirname)
    skipfile_names.write(dirname + "\n")
    conn.close()

if __name__ == '__main__':
    for listing in open('fpid.list2'):
        dirname = listing.rstrip()
        if dirname not in KNOWN_SKIPFILES:
            find_ebooks(dirname)
        else:
            print "Skipping " + dirname
            log.debug("Skipping %s" % dirname)
            
