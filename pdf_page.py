#!/usr/bin/env python

import os, filecmp, shutil, time, math
from pyPdf import PdfFileReader
from numpy import *
from histogram import *

############################################################

def stats(my_year,my_list):
    my_list.sort()
    # Average
    total_pages = 0
    for number in my_list:
        total_pages += number
        ave_pages = float(total_pages)/float(len(my_list))
    # Standard Deviation
    deviation_sq_sum = 0
    for number in my_list:
        deviation_sq_sum += (number - ave_pages)*(number - ave_pages)
        standard_deviation = math.sqrt(float(deviation_sq_sum)/float(len(my_list)))
    # Median
    if len(my_list)%2: #odd
        index = (len(my_list)+1)/2 
        median = float(my_list[index - 1])
    else: #even
        index = len(my_list)/2 
        median = float((my_list[index - 1]+my_list[index]))/2.0
    # Mode
    mode = 0
    mode_freq = 0
    page_dict = {}
    for number in my_list:
        _= page_dict.setdefault(number,0)
        page_dict[number] += 1
    for key in page_dict:
        if mode_freq < page_dict[key]:
            mode_freq = page_dict[key]
            mode = key
    # Error on the Mean
    standard_error = standard_deviation/math.sqrt(len(my_list))
    print "------------------\t---- {} ----\t------------------".format(my_year)
    print "Total number of PDFs\t{:10}".format(len(my_list))
    print "Total Number of pages\t{:10}".format(total_pages)
    print "Largest Book\t{}".format(my_list[len(my_list) - 1])
    print "Standard Deviation\t{:.4}".format(standard_deviation)
    print "Average Number of pages\t{:.4} ".format(ave_pages) + " +/- {:.4}".format(standard_error)
    print "Median Number of pages\t{:.4}".format(median)
    print "Mode Number of pages\t{}\twith frequency {}".format(mode,mode_freq)

############################################################

BASE_DIR = "/home/content/uploaded/pdfs"
BAD_DIR = "/home/content/uploaded/pdfs/badfiles"
GOOD_DIR = "/home/content/uploaded/pdfs/goodfiles"

ignore_dirs = []
ignore_dirs.append(BAD_DIR)

file_list = []
for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            file_list.append(os.path.join(dirpath,files))

year_dict = {}
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
        try:
            file1 = open(files, "rb")
            doc = PdfFileReader(file1)
            page_number = doc.getNumPages()
            if page_number > 2000:
                print "{} {}".format(page_number,files)
            doc_dict = doc.getDocumentInfo()
            doc_date = doc_dict['/CreationDate'][2:6].strip()
            if not doc_date.isdigit():
                doc_date = doc_dict['/CreationDate'].split(' ')[-1].strip()
            if not doc_date.isdigit():
                print doc_dict['/CreationDate']
            year_list = []
            year_list = year_dict.setdefault(doc_date,year_list)
            year_list.append(page_number)
            year_dict[doc_date] = year_list

            num_pages.append(page_number)
        except:
            file2 = os.path.join(BAD_DIR,raw_name)

    file1.close()
    #if counter >= 100:
    #    break

############################################################

under_flow  = 0
over_flow  = 0
hmin = 0.0
hmax = 2000.0
nbins = 40
bin_size = (hmax-hmin)/nbins
bin_center = bin_size/2
h = histogram("h", [('PDF pages', arange(hmin+bin_center,hmax+bin_center,bin_size))])

for value in num_pages:
      if value > hmax:
          over_flow += 1
      elif value <= hmin:
          under_flow += 1
      else:
          bin_value = h[value,value+0.01].I 
          bin_value += 1
          h[value,value+0.01] = bin_value ,None

print 'Number of Pages\t1 SD\t2 SD\t3 SD\t>= 4 SD'
print "> {}\t{}".format('Zero',under_flow)
bin_num = 1
for bins in h.I:
    print "{} - {}\t{}".format(int((bin_num-1)*bin_size),int(bin_num*bin_size),int(bins))
    bin_num += 1
print "> {}\t{}".format(int((bin_num-1)*bin_size),over_flow)

############################################################

under_flow  = 0
over_flow  = 0
hmin = 0.0
hmax = 51.0
nbins = 51
bin_size = (hmax-hmin)/nbins
bin_center = bin_size/2
h2 = histogram("h2", [('PDF pages < 50', arange(hmin+bin_center,hmax+bin_center,bin_size))])

for value in num_pages:
      if value >= hmax:
          over_flow += 1
      elif value <= hmin:
          under_flow += 1
      else:
          bin_value = h2[value,value+0.01].I 
          bin_value += 1
          h2[value,value+0.01] = bin_value ,None

print 'Number of Pages\t1 SD\t2 SD\t3 SD\t>= 4 SD'
print "> {}\t{}".format('Zero',under_flow)
bin_num = 1
for bins in h2.I:
    print "{} - {}\t{}".format(int((bin_num-1)*bin_size),int(bin_num*bin_size),int(bins))
    bin_num += 1
print "> {}\t{}".format(int((bin_num-1)*bin_size),over_flow)

############################################################


stats('Total',num_pages)

sorted_years = sorted(year_dict)
for year in sorted_years:
    year_list = year_dict[year]
    stats(year,year_list)



