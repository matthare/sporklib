#!/usr/bin/env python

import os, filecmp, time
import imghdr, subprocess
from numpy import *
from histogram import *

BASE_DIR = "/home/content/uploaded/covers"
BAD_DIR = "/home/content/uploaded/covers/badfiles"
JPG_DIR = "/home/content/uploaded/covers/goodjpgs"

ignore_dirs = [BAD_DIR,JPG_DIR]

def run(cmd):
    call = ["/bin/bash", "-c", cmd]
    try:
       output = subprocess.check_output(call)
       return output
    except:
       return 'bad EMPTY'

def get_img_size(file1):
    line = run("identify " + file1)
    line_list = line.split(' ')
    image_type = line_list[1]
    if image_type != 'EMPTY':
       size_list = line_list[2].split('x')
       pixels = int(size_list[0])*int(size_list[1])
    else:
       pixels = 0
    return (pixels,image_type)

file_list = []

for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            file_list.append(os.path.join(dirpath,files))

jpg_counter = 0
png_counter = 0
gif_counter = 0
bad_counter = 0
over_counter = 0
hmin = 0.0
hmax = 2000000.0
nbins = 9
bin_list = ['Thumbnail','XXXS','XXS','XS','S','M','L','XL','XXL']
bin_size = (hmax-hmin)/nbins
bin_center = bin_size/2
h = histogram("h", [('Image Size', arange(hmin+bin_center,hmax+bin_center,bin_size))])
tmb_list = []

bin_number = 1
counter = 0
for files in file_list:
    counter += 1
    raw_path,raw_name = os.path.split(files)
    raw_base,raw_ext = os.path.splitext(raw_name)
    base = raw_base.lower()
    ext = raw_ext.lower()

    pixels, image_type = get_img_size(files)
    
    
    if image_type  == 'JPEG' and ext == '.jpg':
       jpg_counter += 1
       
       if pixels > bin_number*bin_size and pixels <= (bin_number + 1)*bin_size:
          tmb_list.append(raw_base)
       
       if pixels > hmax:
          over_counter += 1
       else:
          bin_value = h[pixels,pixels+0.01].I 
          bin_value += 1
          h[pixels,pixels+0.01] = bin_value ,None

    elif image_type  == 'PNG' and ext == '.png':
       png_counter += 1
       
       if pixels > bin_number*bin_size and pixels <= (bin_number + 1)*bin_size:
          tmb_list.append(raw_base)
       
       if pixels > hmax:
          over_counter += 1
       else:
          bin_value = h[pixels,pixels+0.01].I 
          bin_value += 1
          h[pixels,pixels+0.01] = bin_value ,None

    elif image_type  == 'GIF' and ext == '.gif':
       gif_counter += 1
       
       if pixels > bin_number*bin_size and pixels <= (bin_number + 1)*bin_size:
          tmb_list.append(raw_base)
       
       if pixels > hmax:
          over_counter += 1
       else:
          bin_value = h[pixels,pixels+0.01].I 
          bin_value += 1
          h[pixels,pixels+0.01] = bin_value ,None

    else:
       print run("identify " + files)
       bad_counter += 1

f = open('fpidcover.list', 'w')
for item in tmb_list:
   f.write(item + "\n")
f.close()


hdata = h.I
cntr = 0
for bins in hdata:
    cntr += 1
    print str(bin_list[cntr-1])+ "\t" + str(int(bins))
print "XXXL\t" + str(over_counter)


print str(jpg_counter) + " JPGs"
print str(png_counter) + " PNGs"
print str(gif_counter) + " GIFs"
print str(bad_counter) + " bad files"
print str(counter) + " total files"




