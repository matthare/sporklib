#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

BASE_DIR = "/home/content/uploaded"
DUP_DIR = "/home/content/uploaded/duplicates"
OLD_DIR = "/home/content/uploaded/oldbooks"

ignore_dirs.append(DUP_DIR)
ignore_dirs.append(OLD_DIR)
#ignore_dirs.append(os.path.join(BASE_DIR,'docbook'))
#ignore_dirs.append(os.path.join(BASE_DIR,'pdf'))
#ignore_dirs.append(os.path.join(BASE_DIR,'2009'))

dir_list = []
file_list = []

for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for dirs in dirnames:
            dir_list.append(dirs)
        for files in filenames:
            file_list.append(files)

file_dict = {}
name_dict = {}
dup_dict = {}
for files in file_list:
    raw_base,raw_ext = os.path.splitext(files)
    base = raw_base.lower()
    ext = raw_ext.lower()

    #Lets first look to see if any files have the same name.
    if ext == '.epub' or ext == '.pdf' or ext == '.zip':
        _ = dup_dict.setdefault(files.lower(),0)
        dup_dict[files.lower()] += 1

    _ = file_dict.setdefault(ext,0)
    file_dict[ext] += 1

    if ext == '.epub' or ext == '.pdf':
        _ = name_dict.setdefault(base,0)
        name_dict[base] += 1
    elif ext == '.zip':
        if '_docbook' in base:
            base = base.rstrip('_docbook')
            _ = name_dict.setdefault(base,0)
            name_dict[base] += 1
        elif '_dockbook' in base:
            base = base.rstrip('_dockbook')
            _ = name_dict.setdefault(base,0)
            name_dict[base] += 1
        else:
            _ = name_dict.setdefault(base,0)
            name_dict[base] += 1

dup_count = 0
for key in dup_dict:
    filepaths = []
    if dup_dict[key] > 1:
        dup_count += 1
        for dirpath, dirnames, filenames in os.walk(BASE_DIR):
            if dirpath not in ignore_dirs:
                for files in filenames:
                    if files.lower() == key:
                        filepaths.append(os.path.join(dirpath,files))

        if filecmp.cmp(filepaths[0],filepaths[1]):
            print filepaths
            #print os.path.join(DUP_DIR,os.path.split(filepaths[1])[1])
            #shutil.move(filepaths[1],os.path.join(DUP_DIR,os.path.split(filepaths[1])[1]))

        print str(dup_count) + " " + str(filepaths)
        print "created: %s last modified: %s" % (time.ctime(os.path.getctime(filepaths[0])), time.ctime(os.path.getmtime(filepaths[0])))
        print "created: %s last modified: %s" % (time.ctime(os.path.getctime(filepaths[1])), time.ctime(os.path.getmtime(filepaths[1])))
        #shutil.move(filepaths[1],os.path.join(OLD_DIR,os.path.split(filepaths[1])[1]))

    str_docbook = '_dockbook'
    if '.zip' in key:
        if str_docbook in key:
            twinkey = key.rstrip(str_docbook+'.zip')+'.zip' 
            if dup_dict.has_key(twinkey):
                dup_count += 1
                for dirpath, dirnames, filenames in os.walk(BASE_DIR):
                    if dirpath not in ignore_dirs:
                        for files in filenames:
                            if files.lower() == key:
                                filepaths.append(os.path.join(dirpath,files))
                            elif files.lower() == twinkey:
                                filepaths.append(os.path.join(dirpath,files))

                if filecmp.cmp(filepaths[0],filepaths[1]):
                    print filepaths
                    if str_docbook in filepaths[0].lower():
                        print os.path.join(DUP_DIR,os.path.split(filepaths[0])[1])
                        #shutil.move(filepaths[0],os.path.join(DUP_DIR,os.path.split(filepaths[0])[1]))
                    else:
                        print os.path.join(DUP_DIR,os.path.split(filepaths[1])[1])
                        #shutil.move(filepaths[1],os.path.join(DUP_DIR,os.path.split(filepaths[1])[1]))

                print str(dup_count) + " " + str(filepaths)
                print "created: %s last modified: %s" % (time.ctime(os.path.getctime(filepaths[0])), time.ctime(os.path.getmtime(filepaths[0])))
                print "created: %s last modified: %s" % (time.ctime(os.path.getctime(filepaths[1])), time.ctime(os.path.getmtime(filepaths[1])))
                if os.path.getmtime(filepaths[0]) < os.path.getmtime(filepaths[1]):
                    print time.ctime(os.path.getmtime(filepaths[0]))
                    #shutil.move(filepaths[0],os.path.join(OLD_DIR,os.path.split(filepaths[0])[1]))
                else:
                    print time.ctime(os.path.getmtime(filepaths[1]))
                    #shutil.move(filepaths[1],os.path.join(OLD_DIR,os.path.split(filepaths[1])[1]))








histogram = {'one' : 0, 'two' : 0, 'three' :0, 'four' : 0}
for key in name_dict:
    if name_dict[key] == 1:
        histogram['one'] += 1
    elif name_dict[key] == 2:
        histogram['two'] += 1
    elif name_dict[key] == 3:
        histogram['three'] += 1
    elif name_dict[key] > 3:
        histogram['four'] += 1
        print(key)





dir_dict = {'Directories' : 0, '.Directories' : 0}
for dirs in dir_list:
    if dirs[0] == '.':
        dir_dict['.Directories'] += 1
    else:
        dir_dict['Directories'] += 1

for key in dir_dict:
    print "Number of " + key + " = " + str(dir_dict[key])

for key in file_dict:
    print "Number of '" + key + "' Files = " + str(file_dict[key])

print "----------------------------------------------------"

print histogram
