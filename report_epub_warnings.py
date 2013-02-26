#!/usr/bin/env python

import os, filecmp, shutil, time, operator

# open the file from CLassic and read in the FPIDs
# remove none FPID chars
f = open('/home/content/uploaded/epubcheck-3.0/justwarning.log', 'r')

error_dict = {}
file_list = []
image_list = []
font_list = []

mycounter = 0
for line in f:
    error = line.rsplit(':',10)
    file_error = error[1].rsplit('/',10)
    file_name = file_error[2]

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
    
    elist = []
    elist = error_dict.setdefault(key,elist)
    if file_name not in elist:
        elist.append(file_name)
    error_dict[key] = elist

f.close()
error_tup = []
for key in error_dict:
    error_tup.append((key, len(error_dict[key])))

for item in sorted(error_tup, key=lambda tup: tup[1], reverse=True):
    print "warning type: " + item[0] + " occured " + str(item[1]) + " times."
  

