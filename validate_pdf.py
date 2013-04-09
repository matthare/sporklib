#!/usr/bin/env python

import os, filecmp, shutil, time, math
from pyPdf import PdfFileReader
#from pyPDF2 import PdfFileReader 

BASE_DIR = "/home/content/uploaded/pdfs"
BAD_DIR = "/home/content/uploaded/pdfs/badfiles"
GOOD_DIR = "/home/content/uploaded/pdfs/goodfiles"

ignore_dirs = [BAD_DIR,GOOD_DIR]

file_list = []

for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            file_list.append(os.path.join(dirpath,files))

file_dict = {}
name_dict = {}
ext_list = []
num_pages = []
counter = 0
for files in file_list:
    raw_path,raw_name = os.path.split(files)
    raw_base,raw_ext = os.path.splitext(raw_name)
    base = raw_base.lower()
    ext = raw_ext.lower()

    counter += 1

    if ext == '.pdf':
        print "trying " + files
        try:
            file1 = open(files, "rb")
            doc = PdfFileReader(file1)

            num_pages.append(doc.getNumPages())

            file2 = os.path.join(GOOD_DIR,raw_name)
            print "Moving " + files + " to " + file2
            shutil.move(files,file2)
            
        except:
            file2 = os.path.join(BAD_DIR,raw_name)
            print "Moving " + files + " to " + file2
            shutil.move(files,file2)

    file1.close()

total_pages = 0
for number in num_pages:
    total_pages += number
ave_pages = float(total_pages)/float(len(num_pages))
deviation_sq_sum = 0
for number in num_pages:
    deviation_sq_sum += (number - ave_pages)*(number - ave_pages)
standard_deviation = math.sqrt(float(deviation_sq_sum)/float(len(num_pages)))

standard_error = standard_deviation/math.sqrt(len(num_pages))

print "-----------------------------"
print "Total number of PDFs {:10}".format(counter)
print "Total Number of pages {:10}".format(total_pages)
print "Average Number of pages {:.4} ".format(ave_pages) + " +/- {:.4}".format(standard_error)

