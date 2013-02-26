#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

EPUB_DIR = "/home/content/uploaded/epubs"
PDF_DIR = "/home/content/uploaded/pdfs"
DB_DIR = "/home/content/uploaded/zips/docbooks"

ignore_dirs = []
ignore_dirs.append(os.path.join(EPUB_DIR,'error'))
#ignore_dirs.append(os.path.join(EPUB_DIR,'error/accept'))
ignore_dirs.append(os.path.join(EPUB_DIR,'error/reject'))
ignore_dirs.append(os.path.join(PDF_DIR,'badfiles'))

def summary(mylist,mystring):
    print "---------------------------------"
    if mystring == 'Not Found':
        #for item in mylist:
        #    print "Could not find " + item 
        print str(len(mylist)) + " " + mystring
    else:
        #for item in mylist:
        #    print "Found " + item + " in " + mystring
        print "Found " + str(len(mylist)) + " in " + mystring

################################

query_fpid_list = sporklib.get_query_list('./hugelist.txt')

################################

spork_epub_fpid_list , spork_epub_dict = sporklib.get_fpid_list(EPUB_DIR,ignore_dirs)
spork_pdf_fpid_list , spork_pdf_dict = sporklib.get_fpid_list(PDF_DIR,ignore_dirs)
spork_db_fpid_list , spork_db_dict = sporklib.get_fpid_list(DB_DIR,ignore_dirs)

################################

epub_list = []
pdf_list = []
docb_list = []
notf_list = []
out_list = []
for item in query_fpid_list:
    if item in spork_epub_fpid_list:
        epub_list.append(item)
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
summary(pdf_list,'Pdfs')
summary(docb_list,'Docbooks')
summary(notf_list,'Not Found')
print "---------------------------------"

f = open('./fpid.list', 'w')
for item in out_list:
    f.write(item + "\n")
f.close()

