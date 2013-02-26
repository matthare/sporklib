#!/usr/bin/env python

import os, filecmp, shutil, time, zipfile

BASE_DIR = "/home/content/uploaded/zips"
DUP_DIR = "/home/content/uploaded/duplicates"
OLD_DIR = "/home/content/uploaded/oldbooks"
BAD_DIR = "/home/content/uploaded/badfiles"
SAF_DIR = "/home/content/uploaded/safe"

ignore_dirs = [DUP_DIR,OLD_DIR,BAD_DIR,SAF_DIR,'/home/content/uploaded/epubcheck-3.0']
ignore_dirs.append('/home/content/uploaded/zips/docbooks')
ignore_dirs.append('/home/content/uploaded/zips/other')
ignore_dirs.append('/home/content/uploaded/zips/badfiles')

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

zip_xml = []
not_zip_xml = []
for files in path_list:
    raw_base,raw_ext = os.path.splitext(files)
    base = raw_base.lower()
    ext = raw_ext.lower()

    if '.zip' == ext:
        #print files
        try:
            with zipfile.ZipFile(files,'r') as myzip:
                items = myzip.namelist()
                is_db = False
                for item in items:
                    if 'book1.xml' in item or 'book.xml' in item or 'original_xml' in item:
                        is_db = True
                        #print item
                        if files not in zip_xml:
                            zip_xml.append(files)
                if not is_db:
                    not_zip_xml.append(files)
            myzip.close()
        except:
            print "Bad File being moved: " + files
            shutil.move(files,files.replace('zips','zips/badfiles'))
            
not_xml_count = 0
print "Files that do not have a book1.xml file:"
for item in not_zip_xml:
    print item
    shutil.move(item,item.replace('zips','zips/other'))

zip_count = 0
print "Files of zipped up xmls: "
for item in zip_xml:
    print item
    shutil.move(item,item.replace('zips','zips/docbooks'))

print len(not_zip_xml)
print len(zip_xml)
