#!/usr/bin/env python

import os, filecmp, shutil, time

CLEAN_DIR = "/home/content/uploaded/epubs/clean"
WARN_DIR = "/home/content/uploaded/epubs/warning"
ERRA_DIR = "/home/content/uploaded/epubs/error/accept"
ERRR_DIR = "/home/content/uploaded/epubs/error/reject"

def make_lists(base_dir):
    file_list = []
    path_list = []
    for dirpath, dirnames, filenames in os.walk(base_dir):
        for files in filenames:
            file_list.append(files)
            path_list.append(os.path.join(dirpath,files))
    return file_list, path_list

clean_list , clean_path_list = make_lists(CLEAN_DIR)
warn_list , warn_path_list = make_lists(WARN_DIR)
erra_list , erra_path_list = make_lists(ERRA_DIR)
errr_list , errr_path_list = make_lists(ERRR_DIR)


print len(clean_list)
print len(warn_list)
print len(erra_list)
print len(errr_list)

for item in errr_path_list:
    file_name = os.path.split(item)[1]
    if file_name in clean_list:
        print "A " + item
        #os.remove(item)
    elif file_name in warn_list:
        print "B " + item
        #os.remove(item)
    elif file_name in erra_list:
        print "C " + item
        #os.remove(item)

for item in erra_path_list:
    file_name = os.path.split(item)[1]
    if file_name in clean_list:
        print "D " + item
        #os.remove(item)
    elif file_name in warn_list:
        print "E " + item
        #os.remove(item)

for item in warn_path_list:
    file_name = os.path.split(item)[1]
    if file_name in clean_list:
        print "F " + item
        #os.remove(item)
