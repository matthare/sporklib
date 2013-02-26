#!/usr/bin/env python

import os, filecmp, shutil, time
from pyPdf import PdfFileReader
#from pyPDF2 import PdfFileReader 

BASE_DIR = "/home/content/uploaded/pdfs"
BAD_DIR = "/home/content/uploaded/pdfs/badfiles"
GOOD_DIR = "/home/content/uploaded/pdfs/goodfiles"

ignore_dirs = [BAD_DIR,GOOD_DIR]

dir_list = []
file_list = []

for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for dirs in dirnames:
            dir_list.append(dirs)
        for files in filenames:
            file_list.append(os.path.join(dirpath,files))

file_dict = {}
name_dict = {}
ext_list = []
counter = 0
for files in file_list:
    raw_path,raw_name = os.path.split(files)
    raw_base,raw_ext = os.path.splitext(raw_name)
    base = raw_base.lower()
    ext = raw_ext.lower()

    counter += 1

    if ext == '.pdf':
        try:
            file1 = open(files, "rb")
            doc = PdfFileReader(file1)

            file2 = os.path.join(GOOD_DIR,raw_name)
            print "Moving " + files + " to " + file2
            shutil.move(files,file2)
            
        except:
            file2 = os.path.join(BAD_DIR,raw_name)
            print "Moving " + files + " to " + file2
            shutil.move(files,file2)

    file1.close()
