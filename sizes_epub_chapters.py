#!/usr/bin/env python

import os, filecmp, shutil, time, zipfile
from numpy import *
from histogram import *

BASE_DIR = "/home/content/uploaded/epubs"

ignore_dirs = []

path_list = []
for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            path_list.append(os.path.join(dirpath,files))

dbook_epub = []
zip_epub = []
largest = 0

over_flow = 0
under_flow = 0
hmin = 0.0
hmax = 100000000.0
nbins = 100
bin_size = (hmax-hmin)/nbins
bin_center = bin_size/2
h = histogram("h", [('freq', arange(hmin+bin_center,hmax+bin_center,bin_size))])
for files in path_list:
    raw_base,raw_ext = os.path.splitext(files)
    base = raw_base.lower()
    ext = raw_ext.lower()

    if '.epub' == ext:
        fsize = os.path.getsize(files)
        if fsize > largest:
            largest = fsize
            
        chapter = 0
        try:
            with zipfile.ZipFile(files,'r') as myzip:
                items = myzip.namelist()
                for item in items:
                    if item.endswith('.html'):
                        chapter += 1
                    elif item.endswith('.xhtml'):
                        chapter += 1
                    elif item.endswith('.htm'):
                        chapter += 1
                    elif item.endswith('.xml'):
                        chapter += 1
        except:
            print "Bad File being moved: " + files

        if chapter == 0:
            print "{} {} {}".format(files,fsize,chapter)
            continue
        csize = fsize/chapter

        if csize > hmax:
            over_flow += 1
            print files 
        elif csize <= hmin:
            under_flow += 1
        else:
            bin_value = h[csize,csize+0.01].I 
            bin_value += chapter
            h[csize,csize+0.01] = bin_value ,None
        
print "Largest File Size = " + str(largest)
hdata = h.I
counter = 0
for bins in hdata:
    counter += 1
    if bins != 0:
        print str((counter-1)*bin_size/1000000) + "Mb - " + str(counter*bin_size/1000000) + "Mb  = \t" + str(int(bins))

counter += 1
print str((counter-1)*bin_size/1000000) + "Mb - " + str(counter*bin_size/1000000) + "Mb  = \t" + str(int(over_flow))

#print h
#plot(h)
