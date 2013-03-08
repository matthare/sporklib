#!/usr/bin/env python

import os, filecmp, shutil, time

BASE_DIR = "/home/content/uploaded/epubs/error"
ACCEPT_DIR = "/home/content/uploaded/epubs/error/accept"
REJECT_DIR = "/home/content/uploaded/epubs/error/reject"

ignore_dirs = []
ignore_dirs.append(ACCEPT_DIR)
ignore_dirs.append(REJECT_DIR)

# open the file from CLassic and read in the FPIDs
# remove none FPID chars
f = open('/home/content/uploaded/epubcheck-3.0/justerror.log', 'r')

file_moved = []
error_dict = {}
for line in f:
    error = line.rsplit(':',10)
    file_error = error[1].rsplit('/',10)
    for item in file_error:
        if item.endswith('.epub'):
            file_name = item
    
    file1 = os.path.join(BASE_DIR,file_name)

    if file1 not in file_moved:

        error_str = error[2]
        if error_str[0] == ' ':
            error_str = error_str[1:]
        error_id = error_str.rsplit(' ',50)

        it = 3
        while len(error_id) == 1:
            error_str = error[it]
            if error_str[0] == ' ':
                error_str = error_str[1:]
            error_id = error_str.rsplit(' ',50)
            it += 1

        key = error_id[0] + " " + error_id[1]

        if key == 'I/O error':
            file2 = os.path.join(REJECT_DIR,file_name)
            _= error_dict.setdefault(key,0)
            error_dict[key] += 1
        elif key == 'Cannot read':
            file2 = os.path.join(REJECT_DIR,file_name)
            _= error_dict.setdefault(key,0)
            error_dict[key] += 1
        elif key == 'invalid LOC':
            file2 = os.path.join(REJECT_DIR,file_name)
            _= error_dict.setdefault(key,0)
            error_dict[key] += 1
        elif key == 'No rootfile':
            file2 = os.path.join(REJECT_DIR,file_name)
            _= error_dict.setdefault(key,0)
            error_dict[key] += 1
        elif key == 'Premature end':
            file2 = os.path.join(REJECT_DIR,file_name)
            _= error_dict.setdefault(key,0)
            error_dict[key] += 1
        elif key == 'toc attribute':
            file2 = os.path.join(REJECT_DIR,file_name)
            _= error_dict.setdefault(key,0)
            error_dict[key] += 1
        elif key == 'Required META-INF/container.xml':
            file2 = os.path.join(REJECT_DIR,file_name)
            _= error_dict.setdefault(key,0)
            error_dict[key] += 1
        elif key == 'character content':
            file2 = os.path.join(REJECT_DIR,file_name)
            _= error_dict.setdefault(key,0)
            error_dict[key] += 1
        else:        
            file2 = os.path.join(ACCEPT_DIR,file_name)
            _= error_dict.setdefault('Ignore',0)
            error_dict['Ignore'] += 1
            
        if os.path.exists(file1):
            print "Moving " + file1 + " to " + file2
            #shutil.move(file1,file2)
            file_moved.append(file1)
        else:
            print "File " + file1 + " does not exists"
f.close()

for key in error_dict:
    print "error type: " + key + " occured " + str(error_dict[key]) + " times."
