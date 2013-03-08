#!/usr/bin/env python

import os, filecmp, shutil, time

BASE_DIR = "/home/content/uploaded"
DUP_DIR = "/home/content/uploaded/duplicates"
OLD_DIR = "/home/content/uploaded/oldbooks"

ignore_dirs = [DUP_DIR,OLD_DIR, '/home/content/uploaded/badfiles']

dir_list = []
file_list = []

for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for dirs in dirnames:
            dir_list.append(dirs)
        for files in filenames:
            file_list.append(os.path.join(dirpath,files))

for files in file_list:
    raw_base,raw_ext = os.path.splitext(files)
    base = raw_base.lower()
    ext = raw_ext.lower()

    if ext == '.epub' or ext == '.pdf' or ext == '.jpg' or ext == '.zip':
        my_str = 'x'
        if my_str in raw_base:
            if os.path.exists(files.replace(my_str,"X")):
                print files
                print files.replace(my_str,"X")
            else:
                print "Moving " + files + " to " + files.replace(my_str,"X")
                #shutil.move(files,files.replace(my_str,"X"))

        my_str = 'si'
        if my_str in raw_base:
            if os.path.exists(files.replace(my_str,"SI")):
                print files
                print files.replace(my_str,"SI")
            else:
                print "Moving " + files + " to " + files.replace(my_str,"SI")
                #shutil.move(files,files.replace(my_str,"SI"))

    if ext == '.epub' or ext == '.pdf' or ext == '.jpg':
        if '-' in base:
            print files
            print files.replace("-","")
            #shutil.move(files,files.replace("-",""))

    if ext == '.zip':
        if '_dockbook' in base:
            new_base = raw_base.rstrip('_Dockbook')
            new_file = new_base + '.zip'
            if not os.path.exists(new_file):
                shutil.move(files,new_file)
            elif '_docbook' in base:
                new_base = raw_base.rstrip('_Docbook')
            new_file = new_base + '.zip'
            if not os.path.exists(new_file):
                shutil.move(files,new_file)


    elif ext == '.epub':
        if 'urnxdomainoreillycomproduct' in base:
            new_base = raw_base.lstrip('/home/content/uploaded/urnxdomainoreillycomproduct')
            new_base = new_base.rstrip('ip')
            new_file = '/home/content/uploaded/' + new_base + '.epub'
            if not os.path.exists(new_file):
#               shutil.move(files,new_file)
                print files
                print new_file
            elif os.path.exists(new_file):
                if filecmp.cmp(files,new_file):
                    print files
                    print new_file
                    #shutil.move(files,os.path.join(DUP_DIR,os.path.split(files)[1]))

        if 'Batch03' not in base:
            new_base = raw_base.lstrip('/home/content/uploaded/')
            new_file = '/home/content/uploaded/Batch03/' + new_base + '.epub'
            if os.path.exists(new_file):
                print files
                print new_file
                if filecmp.cmp(files,new_file):
                    print files
                    print new_file
                    print os.path.join(DUP_DIR,os.path.split(new_file)[1])
                    #shutil.move(new_file,os.path.join(DUP_DIR,os.path.split(new_file)[1]))


    elif ext == '.pdf':
        if 'urnxdomainoreillycomproduct' in base:
            new_base = raw_base.lstrip('/home/content/uploaded/urnxdomainoreillycomproduct')
            new_base = new_base.rstrip('IP')
            new_file = '/home/content/uploaded/' + new_base + '.pdf'
            if not os.path.exists(new_file):
#                shutil.move(files,new_file)
                print files
                print new_file
            elif os.path.exists(new_file):
                if filecmp.cmp(files,new_file):
                    print files
                    print new_file
                    #shutil.move(files,os.path.join(DUP_DIR,os.path.split(files)[1]))

    elif ext == '.jpg':
        if 'covers' not in base:
            new_base = raw_base.lstrip('/home/content/uploaded/')
            new_file = '/home/content/uploaded/covers/' + new_base + '.jpg'
            if os.path.exists(new_file):
                print files
                print new_file
                if filecmp.cmp(files,new_file):
                    print files
                    print new_file
                    print os.path.join(DUP_DIR,os.path.split(new_file)[1])
                    #shutil.move(new_file,os.path.join(DUP_DIR,os.path.split(new_file)[1]))
