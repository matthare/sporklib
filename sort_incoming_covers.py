#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

BASE_DIR = "/home/content/uploaded/incoming"
COVER_DIR = "/home/content/uploaded/covers"
DUP_DIR = "/home/content/uploaded/duplicates"

ignore_dirs = []
ignore_dirs.append(os.path.join(COVER_DIR,'badfiles'))

# going to have to rename stuff first.


file_list, file_FPID_list , file_dict = sporklib.get_fpid_list(BASE_DIR,ignore_dirs)
cover_list, cover_FPID_list , cover_dict = sporklib.get_fpid_list(COVER_DIR,ignore_dirs)

file_set = set(file_FPID_list)
cover_set = set(cover_FPID_list)

in_doc_not_cover_set = file_set - cover_set
in_doc_and_cover_set = file_set & cover_set

unique_list = [(fpid,filename) for fpid in in_doc_not_cover_set for filename in file_list if fpid in filename]
common_list = [(fpid,filename1,filename2) for fpid in in_doc_and_cover_set for filename1 in file_list for filename2 in cover_list if fpid in filename1 and fpid in filename2]

for item in unique_list:
    _, file_name = os.path.split(item[1])

    file1 = item[1]
    file2 = os.path.join(COVER_DIR,file_name)

    if not os.path.exists(file2):
        print "Moving New file " + file1 + " to " + file2
        #shutil.move(file1,file2)
    else:
        print "ERROR A file " + file_name + " already exists in " + COVER_DIR

for item in common_list:
    _, file_name = os.path.split(item[1])

    file1 = item[1]
    file2 = item[2]
    file3 = os.path.join(DUP_DIR,file_name)
    fsize1 = os.path.getsize(file1)
    fsize2 = os.path.getsize(file2)

    if os.path.exists(file2):
        if filecmp.cmp(file1,file2):
            print "Moving Dup file " + file1 + " to " + file3
            #shutil.move(file1,file3)
        elif fsize1 > fsize2:
            print "Moving Larger file " + file1 + " to " + file2
            #shutil.move(file1,file2)
        else:
            print "Original File  " + file2 + " is being kept."
            #os.remove(file1)
    else:
        print "ERROR A file " + file_name + " does not exist in " + COVER_DIR


