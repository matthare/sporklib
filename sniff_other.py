#!/usr/bin/env python

import os, filecmp, shutil, time, zipfile

BASE_DIR = "/home/content/uploaded/zips/other"

ignore_dirs = []
ignore_dirs.append(os.path.join(BASE_DIR,'epub'))
ignore_dirs.append(os.path.join(BASE_DIR,'pdf'))
ignore_dirs.append(os.path.join(BASE_DIR,'other'))

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
zip_pdf = []
not_zip_epub = []
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
                is_epub = False
                is_pdf = False
                for item in items:
                    if '.epub' in item:
                        is_epub = True
                        #print item
                        if files not in zip_epub:
                            zip_epub.append(files)
                    elif pdf_name in item:
                        is_pdf = True
                        #print item
                        if files not in zip_pdf:
                            zip_pdf.append(files)
                if not is_epub and not is_pdf:
                    not_zip_epub.append(files)
            myzip.close()
        except:
            print "Bad File being moved: " + files
            #shutil.move(files,files.replace('zips','zips/badfiles'))
            
not_epub_count = 0
print "Files that do not have .epub file:"
for item in not_zip_epub:
    print item
    #shutil.move(item,item.replace('other','other/other'))

print "Files of zipped up epubs: "
for item in zip_epub:
    print item
    shutil.move(item,item.replace('other','other/epub'))

print "Files of zipped up pdfs: "
for item in zip_pdf:
    print item
    shutil.move(item,item.replace('other','other/pdf'))

print len(not_zip_epub)
print len(zip_epub)
print len(zip_pdf)
