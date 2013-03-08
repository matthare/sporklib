#!/usr/bin/env python

import os, filecmp, shutil, time

BASE_DIR = "/home/content/uploaded/epubs/warning"

ignore_dirs = []

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

file_FPID_list = []
for files in file_list:
    file_FPID_list.append(os.path.splitext(files)[0])
    print os.path.splitext(files)[0]
