#!/usr/bin/env python

import os, filecmp, shutil, time, zipfile
from numpy import *
from histogram import *

BASE_DIR = "/home/content/uploaded/epubs"
DUP_DIR = "/home/content/uploaded/duplicates"
OLD_DIR = "/home/content/uploaded/oldbooks"
BAD_DIR = "/home/content/uploaded/badfiles"
SAF_DIR = "/home/content/uploaded/safe"

ignore_dirs = [DUP_DIR,OLD_DIR,BAD_DIR,SAF_DIR,'/home/content/uploaded/epubcheck-3.0']

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

dbook_epub = []
zip_epub = []
largest = 0

hmin = 0.0
hmax = 250000000.0
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
            
        bin_value = h[fsize,fsize+0.01].I 
        bin_value += 1
        h[fsize,fsize+0.01] = bin_value ,None
        
print "Largest File Size = " + str(largest)
hdata = h.I
counter = 0
for bins in hdata:
    counter += 1
    if bins != 0:
        print str((counter-1)*bin_size/1000000) + "Mb - " + str(counter*bin_size/1000000) + "Mb  = " + str(int(bins))

#print h
#plot(h)
