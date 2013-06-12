#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

EPUB_DIR = "/home/content/uploaded/epubs"
COVER_DIR = "/home/content/uploaded/covers"
XML_DIR = "/home/content/uploaded/xmls"
STAGE_DIR = "/home/content/uploaded/Cowbird"

ignore_dirs = []
ignore_dirs.append('/home/content/uploaded/epubs/error')
#ignore_dirs.append('/home/content/uploaded/epubs/error/accept')
ignore_dirs.append('/home/content/uploaded/epubs/error/reject')

path_list = []
for dirpath, dirnames, filenames in os.walk(EPUB_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            path_list.append(os.path.join(dirpath,files))

for dirpath, dirnames, filenames in os.walk(COVER_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            path_list.append(os.path.join(dirpath,files))

for dirpath, dirnames, filenames in os.walk(XML_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            path_list.append(os.path.join(dirpath,files))


################################

query_fpid_list = sporklib.get_query_list() 

################################

counter = 0
for item in query_fpid_list:
    files = [x for x in path_list if item in x]
    counter += 1
    sub_counter = 0
    upload = False
    for file1 in files:
        if file1.endswith('.epub'):
            upload = True

    if upload:
        for file1 in files:
            sub_counter += 1
            file2 = os.path.join(STAGE_DIR,os.path.split(file1)[1])
            if os.path.exists(file2):
                print "Already have " + file2                                                                                                                                       
            else:                                                                                                                                                                    
                print "{}.{} Copying {} to {}".format(counter,sub_counter,file1,file2)                                                                                                 
                shutil.copy(file1,file2)                    
