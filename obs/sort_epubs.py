#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

BASE_DIR = "/home/content/uploaded/epubs"
CLEAN_DIR = "/home/content/uploaded/epubs/clean"
WARN_DIR = "/home/content/uploaded/epubs/warning"
ERROR_DIR = "/home/content/uploaded/epubs/error"

ignore_dirs = []
ignore_dirs.append(os.path.join(BASE_DIR,'warning'))
ignore_dirs.append(os.path.join(BASE_DIR,'error'))
ignore_dirs.append(os.path.join(BASE_DIR,'error/accept'))
ignore_dirs.append(os.path.join(BASE_DIR,'error/reject'))

#####################################################
# open the file from CLassic and read in the FPIDs
# remove none FPID chars
f = open(os.path.join(BASE_DIR,'justerror.log'), 'r')

file_moved = []
for line in f:    
    error = line.rsplit(':',10)
    file_error = error[1].rsplit('/',10)
    for item in file_error:
        if item.endswith('.epub'):
            file_name = item

    file1 = os.path.join(BASE_DIR,file_name)
    file2 = os.path.join(ERROR_DIR,file_name)

    if file1 not in file_moved:
        if os.path.exists(file1):
            print "Moving E " + file1 + " to " + file2
            #shutil.move(file1,file2)
            file_moved.append(file1)
        else:
            print "E File " + file1 + " does not exists"
f.close()

#####################################################
# open the file from CLassic and read in the FPIDs
# remove none FPID chars
f = open(os.path.join(BASE_DIR,'justwarning.log'), 'r')

for line in f:
    warn = line.rsplit(':',10)
    file_warn = warn[1].rsplit('/',10)
    for item in file_warn:
        if item.endswith('.epub'):
            file_name = item

    file1 = os.path.join(BASE_DIR,file_name)
    file2 = os.path.join(WARN_DIR,file_name)

    if file1 not in file_moved:
        if os.path.exists(file1):
            print "Moving W " + file1 + " to " + file2
            #shutil.move(file1,file2)
            file_moved.append(file1)
        else:
            print "W File " + file1 + " does not exists"
f.close()

#####################################################

_, epub_FPID_list , epub_dict = sporklib.get_fpid_list(CLEAN_DIR,ignore_dirs)
ignore_dirs.append(CLEAN_DIR)
_, file_FPID_list , file_dict = sporklib.get_fpid_list(BASE_DIR,ignore_dirs)

doc_set = set(file_FPID_list)
epub_set = set(epub_FPID_list)

in_doc_not_epub_set = doc_set - epub_set
in_doc_and_epub_set = doc_set & epub_set

for fpid in in_doc_not_epub_set:
    file_name = fpid + '.epub'
    file1 = os.path.join(BASE_DIR,file_name)
    file2 = os.path.join(CLEAN_DIR,file_name)
    if not os.path.exists(file2):
        print "Moving New " + file1 + " to " + file2
        #shutil.move(file1,file2)
    else:
        print "File " + file2 + " already exists"

for fpid in in_doc_and_epub_set:
    file_name = fpid + '.epub'
    file1 = os.path.join(BASE_DIR,file_name)
    file2 = os.path.join(CLEAN_DIR,file_name)

    ftime1 = os.path.getmtime(file1)
    ftime2 = os.path.getmtime(file2)

    if ftime1 > ftime2:
        file3 = file2
    else:
        file3 = os.path.join('/home/content/uploaded/oldbooks',file_name)

    print "Moving Newer " + file1 + " to " + file3
    #shutil.move(file1,file3)

