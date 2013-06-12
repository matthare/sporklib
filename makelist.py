#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

EPUB_DIR = "/home/content/uploaded/epubs"
PDF_DIR = "/home/content/uploaded/pdfs"
DB_DIR = "/home/content/uploaded/zips/docbooks"

ignore_dirs = []

def print_summary(classic_fpid_list,spork_fpid_list,classic_dict,spork_dict):
    common = set(classic_fpid_list) & set(spork_fpid_list)
    in_classic_not_spork = set(classic_fpid_list) - set(spork_fpid_list)
    in_spork_not_classic = set(spork_fpid_list) - set(classic_fpid_list)

    spork_ctr = 0
    classic_ctr = 0
    for fpid in common:
        if spork_dict[fpid] < classic_dict[fpid]:
            classic_ctr += 1
#            print fpid
        else:
            spork_ctr += 1
            
    print str(len(common)) + " FPIDs common to both Classic and Spork"
    print str(spork_ctr) + " are newer on Spork"
    print str(classic_ctr) + " are newer on Classic"
    print str(len(in_classic_not_spork)) + " FPIDs Unique to Classic"
    print str(len(in_spork_not_classic)) + " FPIDs Unique to Spork"
    for item in in_classic_not_spork:
        print item


################################
#
#query_fpid_list = sporklib.get_query_list('./hugelist.txt')
#
################################
# open the file from CLassic and read in the FPIDs
# remove none FPID chars
f = open('./hugelist.txt', 'r')
#f = open('./booklist.txt', 'r')
fpid_dict = {}
classic_dict = {}
classic_fpid_list = []
for line in f:
    fpid = line.rsplit('\t',3)[0]
    mdate_raw = line.rsplit('\t',3)[2].replace("-"," ")
    if mdate_raw != "          ":
        mdate = time.mktime(time.strptime(mdate_raw,'%Y %m %d'))
    else:
        mdate = None
    my_str = '-'
    if my_str in fpid:
        _ = fpid_dict.setdefault(my_str,0)
        fpid_dict[my_str] += 1
        fpid = fpid.replace(my_str,"")
    my_str = '_'
    if my_str in fpid:
        _ = fpid_dict.setdefault(my_str,0)
        fpid_dict[my_str] += 1
        fpid = fpid.replace(my_str,"")
    my_str = 'x'
    if my_str in fpid:
        _ = fpid_dict.setdefault(my_str,0)
        fpid_dict[my_str] += 1
        fpid = fpid.replace(my_str,"X")
    my_str = 'X'
    if my_str in fpid:
        _ = fpid_dict.setdefault(my_str,0)
        fpid_dict[my_str] += 1

    classic_fpid_list.append(fpid)
    _ = classic_dict.setdefault(fpid,mdate)
f.close()
classic_fpid_list.sort()
#print fpid_dict

################################
_, spork_epub_fpid_list , spork_epub_dict = sporklib.get_fpid_list(EPUB_DIR,ignore_dirs)
_, spork_pdf_fpid_list , spork_pdf_dict = sporklib.get_fpid_list(PDF_DIR,ignore_dirs)
_, spork_db_fpid_list , spork_db_dict = sporklib.get_fpid_list(DB_DIR,ignore_dirs)  

spork_fpid_list = []
spork_fpid_list.extend(spork_epub_fpid_list)
spork_fpid_list.extend(spork_pdf_fpid_list)
spork_fpid_list.extend(spork_db_fpid_list)
spork_set = set(spork_fpid_list)
spork_list = []
spork_dict = {}
for item in spork_set:
    spork_list.append(item)
    if item in spork_epub_dict:
        _ = spork_dict.setdefault(item,spork_epub_dict[item])
    elif item in spork_pdf_dict:
        _ = spork_dict.setdefault(item,spork_pdf_dict[item])
    elif item in spork_db_dict:
        _ = spork_dict.setdefault(item,spork_db_dict[item])
    else:
        print "ERROR: Item in Set but not in any Dictionary!"
        
################################
print "--------- BvD ----------"
print len(classic_fpid_list)
print "------- Summary --------"
print_summary(classic_fpid_list,spork_list,classic_dict,spork_dict)
#print "------- Epub Summary --------"
#print_summary(classic_fpid_list,spork_epub_fpid_list,classic_dict,spork_epub_dict)
#print "------- Pdf Summary --------"
#print_summary(classic_fpid_list,spork_pdf_fpid_list,classic_dict,spork_pdf_dict)
#print "------- DocBook Summary --------"
#print_summary(classic_fpid_list,spork_db_fpid_list,classic_dict,spork_db_dict)
