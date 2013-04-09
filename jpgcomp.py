#!/usr/bin/env python

import os, filecmp, shutil, time

BASE_DIR = "/home/content/uploaded"
DUP_DIR = "/home/content/uploaded/duplicates"
OLD_DIR = "/home/content/uploaded/oldbooks"
BAD_DIR = "/home/content/uploaded/badfiles"

ignore_dirs = [DUP_DIR,OLD_DIR,BAD_DIR]

dir_list = []
file_list = []
path_list = []
for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for dirs in dirnames:
            dir_list.append(dirs)
        for files in filenames:
            file_list.append(files)
            path_list.append(os.path.join(dirpath,files))

file_dict = {}
name_dict = {}
ext_list = []
jpg_list = []
for files in file_list:
    raw_base,raw_ext = os.path.splitext(files)
    base = raw_base.lower()
    ext = raw_ext.lower()

    _ = file_dict.setdefault(ext,0)
    file_dict[ext] += 1
    
    ext_list = []

    if ext == '.epub':
        ext_list = name_dict.setdefault(raw_base,ext_list)
        ext_list.append('.epub')
        name_dict[raw_base] = ext_list
    elif ext == '.pdf':
        ext_list = name_dict.setdefault(raw_base,ext_list)
        ext_list.append('.pdf')
        name_dict[raw_base] = ext_list
    elif ext == '.zip':
        ext_list = name_dict.setdefault(raw_base,ext_list)
        ext_list.append('.zip')
        name_dict[raw_base] = ext_list
    elif ext == '.jpg':
        jpg_list.append(raw_base)

spork_fpid_list = []
for key in name_dict:
    lead = key[:5]
    if lead.isdigit():
        spork_fpid_list.append(key) 
    else:
        spork_fpid_list.append(key) 
        print "This file name does not conform to FPID format: " + key



common = set(jpg_list) & set(spork_fpid_list)
in_jpg_not_spork = set(jpg_list) - set(spork_fpid_list)
in_spork_not_jpg = set(spork_fpid_list) - set(jpg_list)

print str(len(common)) + " FPIDs common to both Jpg and Spork"
print str(len(in_jpg_not_spork)) + " FPIDs Unique to Jpg"
print str(len(in_spork_not_jpg)) + " FPIDs Unique to Spork"
