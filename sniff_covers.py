#!/usr/bin/env python

import os, filecmp, shutil, time, zipfile

BASE_DIR = "/home/content/uploaded/zips"
BASE_DIR = "/home/content/uploaded/epubs"
OUT_DIR =  "/home/content/uploaded/newcovers"

ignore_dirs = []
ignore_dirs.append(os.path.join(BASE_DIR,'badfiles'))
#ignore_dirs.append(os.path.join(BASE_DIR,'pdfs'))
#ignore_dirs.append(os.path.join(BASE_DIR,'dbs'))

file_list = []
path_list = []

for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            file_list.append(files)
            path_list.append(os.path.join(dirpath,files))

zip_jpg = []
zip_files = []
for files in path_list:
    raw_path,raw_name = os.path.split(files)
    raw_base,raw_ext = os.path.splitext(raw_name)
    base = raw_base.lower()
    ext = raw_ext.lower()

    if '.zip' == ext or '.epub' == ext:
        #print files
        try:
            with zipfile.ZipFile(files,'r') as myzip:
                items = myzip.namelist()
                for item in items:
                    if files not in zip_files:
                        if os.path.join(raw_base,raw_base + '.jpg') in item:
                            file1 = os.path.join(raw_base,raw_base + '.jpg')
                            file2 = os.path.join(OUT_DIR,file1)
                            print "Extracting " + file1 + " as " + file2
                            myzip.extract(file1,OUT_DIR)
                            zip_jpg.append(file2)
                            zip_files.append(files)
                        elif os.path.join(raw_base,raw_base + '_large.jpg') in item:
                            file1 = os.path.join(raw_base,raw_base + '_large.jpg')
                            file2 = os.path.join(OUT_DIR,file1)
                            print "Extracting " + file1 + " as " + file2
                            myzip.extract(file1,OUT_DIR)
                            zip_jpg.append(file2)
                            zip_files.append(files)
                        elif os.path.join(raw_base,raw_base + '_lrg.jpg') in item:
                            file1 = os.path.join(raw_base,raw_base + '_lrg.jpg')
                            file2 = os.path.join(OUT_DIR,file1)
                            print "Extracting " + file1 + " as " + file2
                            myzip.extract(file1,OUT_DIR)
                            zip_jpg.append(file2)
                            zip_files.append(files)
                        else:
                            print "Didn't find anything in " + files
            myzip.close()
        except:
            print "Bad File being moved: " + files
            #shutil.move(files,files.replace('','badfiles'))
            
print "Files of zipped up epubs: "
for item in zip_jpg:
    raw_path,raw_name = os.path.split(item)
    raw_base,raw_ext = os.path.splitext(raw_name)

    if '_lrg' in raw_base:
        base = raw_base.replace('_lrg','')
    elif '_large' in raw_base:
        base = raw_base.replace('_large','')
    else:
        base = raw_base 

    file1 = item
    file2 = os.path.join(OUT_DIR,base + ".jpg")
    
    if not os.path.exists(file1):
        print "ERROR File " + file1 + " does not exist"
    elif os.path.exists(file2):
        print "ERROR File " + file2 + " already exists"
    else:
        print "Moving File " + file1 + " to " + file2
        shutil.move(file1,file2)
        os.rmdir(raw_path)

print len(zip_jpg)
print len(path_list)
