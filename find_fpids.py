#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

EPUB_DIR = "/home/content/uploaded/epubs"
CLEAN_DIR = "/home/content/uploaded/epubs/clean"
WARN_DIR = "/home/content/uploaded/epubs/warning"
ERRA_DIR = "/home/content/uploaded/epubs/error/accept"
VIDEO_DIR = "/home/content/uploaded/epubs/videos"
PDF_DIR = "/home/content/uploaded/pdfs"
COVER_DIR = "/home/content/uploaded/covers"
DB_DIR = "/home/content/uploaded/zips/docbooks"

ignore_dirs = []
ignore_dirs.append(os.path.join(EPUB_DIR,'error'))
#ignore_dirs.append(os.path.join(EPUB_DIR,'error/accept'))
ignore_dirs.append(os.path.join(EPUB_DIR,'error/reject'))
ignore_dirs.append(os.path.join(PDF_DIR,'badfiles'))

def summary(mylist,mystring,verbose):
    if 'Not Found' in mystring:
        print "---------------------------------"
        if verbose:
            for item in mylist:
                print "Could not find " + item 
        print str(len(mylist)) + " " + mystring
    elif ' ' in mystring and 'pub' in mystring:
        print unichr(9615) + "--------------------------------"
        if verbose:
            for item in mylist:
                print unichr(8866) + unichr(10230) + "  Found " + item + " in " + mystring
        print unichr(8866) + unichr(10230) + "  Found " + str(len(mylist)) + " in " + mystring
    else:
        print "---------------------------------"
        if verbose:
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
_, spork_epub_v_fpid_list , spork_epub_dict = sporklib.get_fpid_list(VIDEO_DIR,ignore_dirs)
_, spork_pdf_fpid_list , spork_pdf_dict = sporklib.get_fpid_list(PDF_DIR,ignore_dirs)
_, spork_db_fpid_list , spork_db_dict = sporklib.get_fpid_list(DB_DIR,ignore_dirs)
_, spork_cvr_fpid_list , spork_cvr_dict = sporklib.get_fpid_list(COVER_DIR,ignore_dirs)

################################

cover_list = []
notc_list = []
epub_list = []
epub_c_list = []
epub_w_list = []
epub_ea_list = []
epub_v_list = []
pdf_list = []
docb_list = []
notf_list = []
out_list = []
for item in query_fpid_list:
    if item in spork_cvr_fpid_list:
        cover_list.append(item)
    else:
        notc_list.append(item)

    if item in spork_epub_fpid_list:
        epub_list.append(item)

    if item in spork_epub_c_fpid_list:
        epub_c_list.append(item)
    elif item in spork_epub_w_fpid_list:
        epub_w_list.append(item)
    elif item in spork_epub_ea_fpid_list:
        epub_ea_list.append(item)
    elif item in spork_epub_v_fpid_list:
        epub_v_list.append(item)

    elif item in spork_pdf_fpid_list:
        pdf_list.append(item)
        out_list.append(item)
    elif item in spork_db_fpid_list:
        docb_list.append(item)
        out_list.append(item)
    else:
        notf_list.append(item)
        out_list.append(item)

summary(epub_list,'Epubs',False)
summary(epub_c_list,'Clean Epubs',True)
summary(epub_w_list,'Epubs w/ Warnings',True)
summary(epub_ea_list,'Epubs w/ Acceptable Errors',True)
summary(epub_v_list,'Video Epubs',False)
summary(pdf_list,'Pdfs',True)
summary(docb_list,'Docbooks',True)
summary(notf_list,'Books Not Found',True)
summary(cover_list,'Covers',False)
summary(notc_list,'Covers Not Found',False)
print "---------------------------------"

f = open('./fpid.list', 'w')
for item in out_list:
    f.write(item + "\n")
f.close()

