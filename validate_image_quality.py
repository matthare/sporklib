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
    output = run("identify -verbose " + file1).split('\n')
    for line in output:
        image_L = 0
        image_W = 0
        exif_L = 0
        exif_W = 0
        tainted = 'False'
        if 'geometry' in line:
            geometry_raw = line.split()[2]
            geometry = geometry_raw.split('+')[0]
            image_L = geometry.split('x')[1]
            image_W = geometry.split('x')[0]

        if 'exif:ExifImageLength' in line:
            exif_L = line.split()[1]

        if 'exif:ExifImageWidth' in line:
            exif_W = line.split()[1]

        if 'Tainted' in line:
            tainted = line.split()[1]

    return (image_L,image_W,exif_L,exif_W,tainted)

file_list = []
with open('filelist','r') as f:
    for line in f:
        file_list.append(line)

for my_file in file_list:
    raw_path,raw_name = os.path.split(my_file)
    raw_base,raw_ext = os.path.splitext(raw_name)
    base = raw_base.lower()
    ext = raw_ext.lower()

    I_Length,I_Width,E_Length,E_Width,tainted = get_img_size(my_file)

    if I_Length > E_Length or I_Width > E_Width:
        print myfile
        print I_Length
        print I_Width
        print E_Length
        print E_Width
