#!/usr/bin/env python

import os, filecmp, shutil, time

BASE_DIR = "/home/content/uploaded"
DUP_DIR = "/home/content/uploaded/duplicates"
OLD_DIR = "/home/content/uploaded/oldbooks"
BAD_DIR = "/home/content/uploaded/badfiles"

ignore_dirs = [DUP_DIR,OLD_DIR,BAD_DIR]

dir_list = []
file_list = []

for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for dirs in dirnames:
            dir_list.append(dirs)
        for files in filenames:
            file_list.append(files)

file_dict = {}
name_dict = {}
ext_list = []
for files in file_list:
    raw_base,raw_ext = os.path.splitext(files)
    base = raw_base.lower()
    ext = raw_ext.lower()

    _ = file_dict.setdefault(ext,0)
    file_dict[ext] += 1
    
    ext_list = []

    if ext == '.epub':
        ext_list = name_dict.setdefault(base,ext_list)
        ext_list.append('.epub')
        name_dict[base] = ext_list
    elif ext == '.pdf':
        ext_list = name_dict.setdefault(base,ext_list)
        ext_list.append('.pdf')
        name_dict[base] = ext_list
    elif ext == '.zip':
        ext_list = name_dict.setdefault(base,ext_list)
        ext_list.append('.zip')
        name_dict[base] = ext_list


histogram = {'epubs' : 0, 'pdfs' : 0, 'dbooks' : 0,
             'epub_only' : 0, 'pdf_only' : 0, 'dbook_only' : 0,
             'epub_pdf' : 0, 'epub_dbook' : 0, 'pdf_dbook' :0,
             'epub_pdf_dbook' : 0}

for key in name_dict:
    if '-' in key:
        print key
    if '.epub' in name_dict[key]:
        histogram['epubs'] +=1

    if '.pdf' in name_dict[key]:
        histogram['pdfs'] +=1

    if '.zip' in name_dict[key]:
        histogram['dbooks'] +=1

    if '.epub' in name_dict[key]     and '.pdf' not in name_dict[key] and'.zip' not in name_dict[key]:
        histogram['epub_only'] +=1
    if '.epub' not in name_dict[key] and '.pdf' in name_dict[key]     and'.zip' not in name_dict[key]:
        histogram['pdf_only'] +=1
    if '.epub' not in name_dict[key] and '.pdf' not in name_dict[key] and'.zip' in name_dict[key]:
        histogram['dbook_only'] +=1

    if '.epub' in name_dict[key]     and '.pdf' in name_dict[key]     and'.zip' not in name_dict[key]:
        histogram['epub_pdf'] +=1
    if '.epub' not in name_dict[key] and '.pdf' in name_dict[key]     and'.zip' in name_dict[key]:
        histogram['pdf_dbook'] +=1
    if '.epub' in name_dict[key]     and '.pdf' not in name_dict[key] and'.zip' in name_dict[key]:
        histogram['epub_dbook'] +=1

    if '.epub' in name_dict[key] and '.pdf' in name_dict[key] and'.zip' in name_dict[key]:
        histogram['epub_pdf_dbook'] +=1

        



dir_dict = {'Directories' : 0, '.Directories' : 0}
for dirs in dir_list:
    if dirs[0] == '.':
        dir_dict['.Directories'] += 1
    else:
        dir_dict['Directories'] += 1

for key in dir_dict:
    print "Number of " + key + " = " + str(dir_dict[key])

for key in file_dict:
    print "Number of '" + key + "' Files = " + str(file_dict[key])

print "----------------------------------------------------"

for key in sorted(histogram):
    print "Number of " + key + " = " + str(histogram[key])
    
