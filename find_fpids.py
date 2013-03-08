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

def summary(mylist,mystring):
    if mystring == 'Not Found':
        print "---------------------------------"
        for item in mylist:
            print "Could not find " + item 
        print str(len(mylist)) + " " + mystring
    elif ' ' in mystring:
        print unichr(9615) + "--------------------------------"
        for item in mylist:
            print unichr(8866) + unichr(10230) + "  Found " + item + " in " + mystring
        print unichr(8866) + unichr(10230) + "  Found " + str(len(mylist)) + " in " + mystring
    else:
        print "---------------------------------"
        for item in mylist:
            print "Found " + item + " in " + mystring
        print "Found " + str(len(mylist)) + " in " + mystring

################################

query_fpid_list = sporklib.get_query_list()

################################

_, spork_epub_fpid_list , spork_epub_dict = sporklib.get_fpid_list(EPUB_DIR,ignore_dirs)
_, spork_epub_c_fpid_list , spork_epub_dict = sporklib.get_fpid_list(CLEAN_DIR,ignore_dirs)
_, spork_epub_w_fpid_list , spork_epub_dict = sporklib.get_fpid_list(WARN_DIR,ignore_dirs)
_, spork_epub_ea_fpid_list , spork_epub_dict = sporklib.get_fpid_list(ERRA_DIR,ignore_dirs)
_, spork_pdf_fpid_list , spork_pdf_dict = sporklib.get_fpid_list(PDF_DIR,ignore_dirs)
_, spork_db_fpid_list , spork_db_dict = sporklib.get_fpid_list(DB_DIR,ignore_dirs)

################################

epub_list = []
epub_c_list = []
epub_w_list = []
epub_ea_list = []
pdf_list = []
docb_list = []
notf_list = []
out_list = []
for item in query_fpid_list:
    if item in spork_epub_fpid_list:
        epub_list.append(item)

    if item in spork_epub_c_fpid_list:
        epub_c_list.append(item)
    elif item in spork_epub_w_fpid_list:
        epub_w_list.append(item)
    elif item in spork_epub_ea_fpid_list:
        epub_ea_list.append(item)

    elif item in spork_pdf_fpid_list:
        pdf_list.append(item)
        out_list.append(item)
    elif item in spork_db_fpid_list:
        docb_list.append(item)
        out_list.append(item)
    else:
        notf_list.append(item)
        out_list.append(item)

summary(epub_list,'Epubs')
summary(epub_c_list,'Clean Epubs')
summary(epub_w_list,'Epubs w/ Warnings')
summary(epub_ea_list,'Epubs w/ Acceptable Errors')
summary(pdf_list,'Pdfs')
summary(docb_list,'Docbooks')
summary(notf_list,'Not Found')
print "---------------------------------"

f = open('./fpid.list', 'w')
for item in out_list:
    f.write(item + "\n")
f.close()

