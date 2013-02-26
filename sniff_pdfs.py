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

zip_pdf = []
for files in path_list:
    raw_dir,raw_file = os.path.split(files)
    raw_name,raw_ext = os.path.splitext(raw_file)
    base = raw_name.lower()
    ext = raw_ext.lower()
    pdf_name = raw_name + '.pdf'

    if '.zip' == ext:
        #print files
        try:
            with zipfile.ZipFile(files,'r') as myzip:
                items = myzip.namelist()
                for item in items:
                    if pdf_name in item:
                        #print item
                        if files not in zip_pdf:
                            zip_pdf.append(files)
                    elif 'singlepdf' in item and '.pdf' in item:
                        print item
            myzip.close()
        except:
            print "Bad File being moved: " + files
            #shutil.move(files,files.replace('','badfiles'))
            
print "Files of zipped up pdfs: "
for item in zip_pdf:
    print item
    #shutil.move(item,item.replace('docbooks','docbooks/pdfs'))

print len(zip_pdf)
print len(path_list)
