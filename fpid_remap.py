#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

EPUB_DIR = "/home/content/uploaded/epubs"
CLEAN_DIR = "/home/content/uploaded/epubs/clean"
WARN_DIR = "/home/content/uploaded/epubs/warning"
ERRA_DIR = "/home/content/uploaded/epubs/error/accept"
PDF_DIR = "/home/content/uploaded/pdfs"
DB_DIR = "/home/content/uploaded/zips/docbooks"

ignore_dirs = []
ignore_dirs.append(os.path.join(EPUB_DIR,'error'))
#ignore_dirs.append(os.path.join(EPUB_DIR,'error/accept'))
ignore_dirs.append(os.path.join(EPUB_DIR,'error/reject'))
ignore_dirs.append(os.path.join(PDF_DIR,'badfiles'))

################################

f = open('fpid.map', 'r')
fpid_list = []
for line in f:
    new_line = line.rstrip()
    fpid_old,fpid_new = new_line.rsplit(',')
    fpid_list.append((fpid_old,fpid_new))
f.close()

################################

spork_epub_list, spork_epub_fpid_list , _ = sporklib.get_fpid_list(EPUB_DIR,ignore_dirs)
spork_pdf_list, spork_pdf_fpid_list , _ = sporklib.get_fpid_list(PDF_DIR,ignore_dirs)
spork_db_list, spork_db_fpid_list , _ = sporklib.get_fpid_list(DB_DIR,ignore_dirs)

################################

spork_file_list = []
spork_file_list.extend(spork_epub_list)
spork_file_list.extend(spork_pdf_list)
spork_file_list.extend(spork_db_list)

epub_list = []
pdf_list = []
docb_list = []
notf_list = []
out_list = []
for twople in fpid_list:
    item1 = twople[0]
    item2 = twople[1]
    files = [x for x in spork_file_list if item1 in x]

    #print item1 + " -> " + item2 
    for file1 in files:
        file2 = file1.replace(item1,item2)
        if not os.path.exists(file1):
            print "ERROR File " + file1 + " does not exist"
        if os.path.exists(file2):
            if filecmp.cmp(file1,file2):
                print "WARNING File " + file1 + " and " + file2 + " are the same"
                #os.remove(file1)
            else:
                ftime1 = os.path.getmtime(file1)
                ftime2 = os.path.getmtime(file2)
                if ftime1 + 604800 < ftime2:
                    print "Warning File " + file2 + " is much newer "
                    print "than " + file1
                    #os.remove(file1)
                elif ftime2 + 604800 < ftime1:
                    print "Warning File " + file1 + " is much newer "
                    print "than " + file2
                    #shutil.move(file1,file2)
                else:
                    print "ERROR File " + file1 + " and " + file2 + " are not the same"
                    print time.ctime(ftime1)
                    print time.ctime(ftime2)
                    #os.remove(file1)
        else:
            print "Renaming " + file1 + " to " + file2
            #shutil.move(file1,file2)
print "---------------------------------"

