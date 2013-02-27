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


OUTFILE_NAME = os.path.join('out', 'datastore_audit.csv')
outfile = csv.writer(open(OUTFILE_NAME, 'a'))

SKIPFILES = 'skipids.txt'
KNOWN_SKIPFILES = set()

if os.path.exists(SKIPFILES):
    for line in open(SKIPFILES, 'r'):
        KNOWN_SKIPFILES.add(line.strip())

# Set this up for appending
skipfile_names = open(SKIPFILES, 'a', 0) # write the skipfiles unbuffered


def find_ebooks(dirname):
    conn = ftplib.FTP(DATASTORE, DATASTORE_USERNAME, DATASTORE_PASSWORD, '', 10)
    conn.set_debuglevel(2)
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    conn.retrlines('LIST %s' % dirname)
    sys.stdout = old_stdout
    found_match = False

    for listing in mystdout.getvalue().split("\n"):
        filename = listing.split(' ')[-1].strip()
        if filename.endswith('pdf') or filename.endswith('epub'):
            log.info("Got filename %s" % filename)
            outfile.writerow([filename, dirname])
            found_match = True
    if not found_match:
        log.info("Didn't find a PDF or an EPUB for %s" % dirname)
    skipfile_names.write(dirname + "\n")
    conn.close()

if __name__ == '__main__':
    for listing in open('dir.txt'):
        dirname = listing.split(' ')[-1].strip()
        if dirname not in KNOWN_SKIPFILES:
            if re.match(r'[0-9]{5}', dirname):
                find_ebooks(dirname)
        else:
            log.debug("Skipping %s" % dirname)
            
