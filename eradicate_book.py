#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

EPUB_DIR = "/home/content/uploaded/epubs"
PDF_DIR = "/home/content/uploaded/pdfs"
COVER_DIR = "/home/content/uploaded/covers"
XML_DIR = "/home/content/uploaded/xmls"
STAGE_DIR = "/home/content/uploaded/Cowbird"

ignore_dirs = []
ignore_dirs.append('/home/content/uploaded/epubs/error')
#ignore_dirs.append('/home/content/uploaded/epubs/error/accept')
ignore_dirs.append('/home/content/uploaded/epubs/error/reject')

path_list = []
for dirpath, dirnames, filenames in os.walk(EPUB_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            path_list.append(os.path.join(dirpath,files))

for dirpath, dirnames, filenames in os.walk(PDF_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            path_list.append(os.path.join(dirpath,files))

for dirpath, dirnames, filenames in os.walk(COVER_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            path_list.append(os.path.join(dirpath,files))

for dirpath, dirnames, filenames in os.walk(XML_DIR):
    if dirpath not in ignore_dirs:
        for files in filenames:
            path_list.append(os.path.join(dirpath,files))


################################

query_fpid_list = sporklib.get_query_list() 

################################

counter = 0
for item in query_fpid_list:
    files = [x for x in path_list if item in x]
    counter += 1
    sub_counter = 0

    has_epub = False
    has_pdf = False
    has_xml = False
    has_cover = False

    for file1 in files:
        if file1.endswith('.epub'):
            has_epub = True
        elif file1.endswith('.pdf'):
            has_pdf = True
        elif file1.endswith('.xml'):
            has_xml = True
        elif file1.endswith('.jpg'):
            has_cover = True

    if not has_epub:
        print "--------------------------------------------> Missing Epub     for {}".format(item)

    if not has_pdf:
        print "--------------------------------------------> Missing Pdf      for {}".format(item)

    if not has_xml:
        print "--------------------------------------------> Missing Metadata for {}".format(item)

    if not has_cover:
        print "--------------------------------------------> Missing Cover    for {}".format(item)


    for file1 in files:
        sub_counter += 1
        if os.path.exists(file1):
            print "{}.{} Removing {}".format(counter,sub_counter,file1)                                                                                                 
            #os.remove(file1)                    

