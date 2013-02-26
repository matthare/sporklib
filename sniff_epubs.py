#!/usr/bin/env python

import os, filecmp, shutil, time, zipfile

BASE_DIR = "/home/content/uploaded/zips/docbooks"

ignore_dirs = []
ignore_dirs.append(os.path.join(BASE_DIR,'epubs'))
ignore_dirs.append(os.path.join(BASE_DIR,'pdfs'))
ignore_dirs.append(os.path.join(BASE_DIR,'dbs'))

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

zip_epub = []
for files in path_list:
    raw_base,raw_ext = os.path.splitext(files)
    base = raw_base.lower()
    ext = raw_ext.lower()

    if '.zip' == ext:
        #print files
        try:
            with zipfile.ZipFile(files,'r') as myzip:
                items = myzip.namelist()
                for item in items:
                    if '.epub' in item:
                        #print item
                        if files not in zip_epub:
                            zip_epub.append(files)
            myzip.close()
        except:
            print "Bad File being moved: " + files
            #shutil.move(files,files.replace('','badfiles'))
            
print "Files of zipped up epubs: "
for item in zip_epub:
    print item
    #shutil.move(item,item.replace('docbooks','docbooks/epubs'))

print len(zip_epub)
print len(path_list)
