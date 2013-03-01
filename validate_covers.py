#!/usr/bin/env python

import os, filecmp, shutil, time
import imghdr, subprocess
from numpy import *
from histogram import *

BASE_DIR = "/home/content/uploaded/covers"
BAD_DIR = "/home/content/uploaded/covers/badfiles"
JPG_DIR = "/home/content/uploaded/covers/goodjpgs"

ignore_dirs = [BAD_DIR,JPG_DIR]

def run(cmd):
   call = ["/bin/bash", "-c", cmd]
   ret = subprocess.call(call, stdout=f, stderr=f)

file_list = []

for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            file_list.append(os.path.join(dirpath,files))

counter = 0
f = open('covers.log', 'w')
for files in file_list:
    raw_path,raw_name = os.path.split(files)
    raw_base,raw_ext = os.path.splitext(raw_name)
    base = raw_base.lower()
    ext = raw_ext.lower()

    counter += 1

    if ext == '.jpg':
       run("identify " + files)

f.close()


jpg_counter = 0
bad_counter = 0
over_counter = 0
hmin = 0.0
hmax = 2000000.0
nbins = 9
bin_list = ['Thumbnail','XXXS','XXS','XS','S','M','L','XL','XXL']
bin_size = (hmax-hmin)/nbins
bin_center = bin_size/2
h = histogram("h", [('Image Size', arange(hmin+bin_center,hmax+bin_center,bin_size))])

f = open('covers.log', 'r')
for line in f:
    line_list = line.split(' ')

    if line_list[1] == 'JPEG':
       jpg_counter += 1
       size_list = line_list[2].split('x')
       pixels = int(size_list[0])*int(size_list[1])
       

       if pixels > hmax:
          over_counter += 1
          #print str(pixels) + " = " + line_list[2]
       else:
          bin_value = h[pixels,pixels+0.01].I 
          bin_value += 1
          h[pixels,pixels+0.01] = bin_value ,None

    else:
       #print line_list[1]
       bad_counter += 1
       

f.close()

hdata = h.I
cntr = 0
for bins in hdata:
    cntr += 1
    print str(bin_list[cntr-1])+ "\t" + str(int(bins))
print "XXXL\t" + str(over_counter)


print str(jpg_counter) + " JPGs"
print str(bad_counter) + " bad files"
print str(counter) + " total files"




