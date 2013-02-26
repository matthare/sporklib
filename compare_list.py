#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

EPUB_DIR = "/home/content/uploaded/epubs"
ignore_dirs = []
ignore_dirs.append('/home/content/uploaded/epubs/error')
#ignore_dirs.append('/home/content/uploaded/epubs/error/accept')
ignore_dirs.append('/home/content/uploaded/epubs/error/reject')
ignore_dirs.append('/home/content/uploaded/pdfs/badfiles')

def print_summary(query_fpid_list,spork_fpid_list,query_dict,spork_dict):
    common = set(query_fpid_list) & set(spork_fpid_list)
    in_query_not_spork = set(query_fpid_list) - set(spork_fpid_list)
    in_spork_not_query = set(spork_fpid_list) - set(query_fpid_list)

    print str(len(common)) + " FPIDs common to both Query and Spork"
    print str(len(in_query_not_spork)) + " FPIDs Unique to Query"
    print str(len(in_spork_not_query)) + " FPIDs Unique to Spork"
    for fpid in in_query_not_spork:
        print fpid

################################

query_dict = {}
query_fpid_list = sporklib.get_query_list()

################################

spork_epub_fpid_list , spork_epub_dict = sporklib.get_fpid_list(EPUB_DIR,ignore_dirs)
#spork_pdf_fpid_list , spork_pdf_dict = sporklib.get_fpid_list(PDF_DIR,ignore_dirs)
#spork_db_fpid_list , spork_db_dict = sporklib.get_fpid_list(DB_DIR,ignore_dirs)

spork_fpid_list = []
spork_fpid_list.extend(spork_epub_fpid_list)
#spork_fpid_list.extend(spork_pdf_fpid_list)
#spork_fpid_list.extend(spork_db_fpid_list)
spork_set = set(spork_fpid_list)
spork_list = []
spork_dict = {}

for item in spork_set:
    spork_list.append(item)
    if item in spork_epub_dict:
        _ = spork_dict.setdefault(item,spork_epub_dict[item])
#    elif item in spork_pdf_dict:
#        _ = spork_dict.setdefault(item,spork_pdf_dict[item])
#    elif item in spork_db_dict:
#        _ = spork_dict.setdefault(item,spork_db_dict[item])
    else:
        print "ERROR: Item in Set but not in any Dictionary!"
        
################################
#print "------- Summary --------"
#print_summary(query_fpid_list,spork_list,query_dict,spork_dict)
print "------- Epub Summary --------"
print_summary(query_fpid_list,spork_epub_fpid_list,query_dict,spork_epub_dict)
#print "------- Pdf Summary --------"
#print_summary(query_fpid_list,spork_pdf_fpid_list,query_dict,spork_pdf_dict)
#print "------- DocBook Summary --------"
#print_summary(query_fpid_list,spork_db_fpid_list,query_dict,spork_db_dict)
