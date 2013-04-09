#!/usr/bin/env python

import os, filecmp, shutil, time
import subprocess

BASE_DIR = "/home/content/uploaded/epubs"

ignore_dirs = []
ignore_dirs.append(BASE_DIR)
ignore_dirs.append(os.path.join(BASE_DIR,'clean'))
ignore_dirs.append(os.path.join(BASE_DIR,'warning'))
ignore_dirs.append(os.path.join(BASE_DIR,'error'))
#ignore_dirs.append(os.path.join(BASE_DIR,'error/accept'))
ignore_dirs.append(os.path.join(BASE_DIR,'error/reject'))


def run(cmd):
   call = ["/bin/bash", "-c", cmd]
   ret = subprocess.call(call, stdout=f, stderr=f)

file_list = []
for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            file_list.append(os.path.join(dirpath,files))

counter = 0
f = open('/home/content/uploaded/epubcheck-3.0/error_accept.log', 'w')
for files in file_list:
    raw_path,raw_name = os.path.split(files)
    raw_base,raw_ext = os.path.splitext(raw_name)
    base = raw_base.lower()
    ext = raw_ext.lower()

    counter += 1

    if ext == '.epub':
        run("java -jar /home/content/uploaded/epubcheck-3.0/epubcheck-3.0.jar " + files)
        
f.close()
