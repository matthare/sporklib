#!/usr/bin/env python

import os, filecmp, shutil, time
import subprocess

BASE_DIR = "/home/content/uploaded/epubs"
REJECT_DIR = "/home/content/uploaded/epubs/error/reject"
ACCEPT_DIR = "/home/content/uploaded/epubs/error/accept"
WARNING_DIR = "/home/content/uploaded/epubs/warning"
CLEAN_DIR = "/home/content/uploaded/epubs/clean"
DUP_DIR = "/home/content/uploaded/duplicates"

ignore_dirs = []
ignore_dirs.append(os.path.join(BASE_DIR,'clean'))
ignore_dirs.append(os.path.join(BASE_DIR,'warning'))
ignore_dirs.append(os.path.join(BASE_DIR,'error'))
ignore_dirs.append(os.path.join(BASE_DIR,'error/accept'))
ignore_dirs.append(os.path.join(BASE_DIR,'error/reject'))


def run(cmd):
   call = ["/bin/bash", "-c", cmd]
   output = ''
   try:
      output = subprocess.check_output(call,stderr=subprocess.STDOUT)
      return output   
   except subprocess.CalledProcessError as file_error:
      return file_error.output

file_list = []
for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            file_list.append(os.path.join(dirpath,files))

counter = 0
for files in file_list:
    raw_path,raw_name = os.path.split(files)
    raw_base,raw_ext = os.path.splitext(raw_name)
    base = raw_base.lower()
    ext = raw_ext.lower()

    counter += 1

    if ext == '.epub':
       output = run("java -jar /home/mhare/sporklib/uploaded/epubcheck-3.0/epubcheck-3.0.jar " + files)
       if 'ERROR:' in output:

          if 'I/O error' in output:
             file2 = os.path.join(REJECT_DIR,raw_name)
          elif 'Cannot read' in output:
             file2 = os.path.join(REJECT_DIR,raw_name)
          elif 'invalid LOC' in output:
             file2 = os.path.join(REJECT_DIR,raw_name)
          elif 'No rootfile' in output:
             file2 = os.path.join(REJECT_DIR,raw_name)
          elif 'Premature end' in output:
             file2 = os.path.join(REJECT_DIR,raw_name)
          elif 'toc attribute' in output:
            file2 = os.path.join(REJECT_DIR,raw_name)
          elif 'Required META-INF/container.xml' in output:
             file2 = os.path.join(REJECT_DIR,raw_name)
          elif 'character content' in output:
             file2 = os.path.join(REJECT_DIR,raw_name)
          else:
             file2 = os.path.join(ACCEPT_DIR,raw_name)

       elif 'WARNING:' in output:
          file2 = os.path.join(WARNING_DIR,raw_name)
       else:
          file2 = os.path.join(CLEAN_DIR,raw_name)

       if not os.path.exists(files):
          print "Error: file " + files + " does not exist"
       elif os.path.exists(file2):
          print "Error: file " + file2 + " already exists"
          if filecmp.cmp(files,file2):
             print "But both are the same, moving {} to Duplicates".format(files)
             file2 = os.path.join(DUP_DIR,raw_name)
             shutil.move(files,file2)
       else:
          print "Moving File " + files + " to " + file2
          shutil.move(files,file2)

