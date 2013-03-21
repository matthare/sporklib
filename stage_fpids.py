#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

EPUB_DIR = "/home/content/uploaded/epubs"
STAGE_DIR = "/home/content/uploaded/Cowbird"

ignore_dirs = []
ignore_dirs.append('/home/content/uploaded/epubs/error')
#ignore_dirs.append('/home/content/uploaded/epubs/error/accept')
ignore_dirs.append('/home/content/uploaded/epubs/error/reject')

dir_list = []
file_list = []
path_list = []
for dirpath, dirnames, filenames in os.walk(EPUB_DIR):
    if dirpath not in ignore_dirs:
        for dirs in dirnames:
            dir_list.append(dirs)
        for files in filenames:
            file_list.append(files)
            path_list.append(os.path.join(dirpath,files))

################################

query_fpid_list = sporklib.get_query_list() 

################################

counter = 0
for item in query_fpid_list:
    for file1 in path_list:
        if item in file1:
            counter += 1
            file2 = os.path.join(STAGE_DIR,os.path.split(file1)[1])
            if os.path.exists(file2):
                print "Already have " + file2
            else:
                print str(counter) + " Copying " + file1 + " to " + file2
                shutil.copy(file1,file2)


