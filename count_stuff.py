#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

EPUB_DIR = "/home/content/uploaded/epubs"
PDF_DIR = "/home/content/uploaded/pdfs"
DBOOK_DIR = "/home/content/uploaded/zips/docbooks"
COVER_DIR = "/home/content/uploaded/covers"

ignore_dirs = []
ignore_dirs.append('/home/content/uploaded/epubs/error/reject')
ignore_dirs.append('/home/content/uploaded/pdfs/badfiles')

epub_list, epub_FPID_list , epub_dict = sporklib.get_fpid_list(EPUB_DIR,ignore_dirs)
pdf_list, pdf_FPID_list , pdf_dict = sporklib.get_fpid_list(PDF_DIR,ignore_dirs)
dbook_list, dbook_FPID_list , dbook_dict = sporklib.get_fpid_list(DBOOK_DIR,ignore_dirs)
cover_list, cover_FPID_list , cover_dict = sporklib.get_fpid_list(COVER_DIR,ignore_dirs)

epub_set = set(epub_FPID_list)
pdf_set = set(pdf_FPID_list)
dbook_set = set(dbook_FPID_list)
cover_set = set(cover_FPID_list)

epub_not_pdf_set = epub_set - pdf_set
epub_and_pdf_set = epub_set & pdf_set
epub_not_dbook_set = epub_set - dbook_set
unique_epub_set = epub_not_pdf_set - dbook_set

pdf_not_dbook_set = pdf_set - dbook_set
pdf_and_dbook_set = pdf_set & dbook_set
pdf_not_epub_set = pdf_set - epub_set
unique_pdf_set = pdf_not_dbook_set - epub_set

dbook_not_epub_set = dbook_set - epub_set
dbook_and_epub_set = dbook_set & epub_set
dbook_not_pdf_set = dbook_set - pdf_set
unique_dbook_set = dbook_not_epub_set - pdf_set

common_set = epub_set & pdf_set & dbook_set

unique_cover_set = cover_set - epub_set - pdf_set - dbook_set
epub_cover_set = cover_set & epub_set
pdf_cover_set = cover_set & pdf_set
dbook_cover_set = cover_set & dbook_set

epub_missing_cover_set = epub_set - cover_set
pdf_missing_cover_set = pdf_set - cover_set
dbook_missing_cover_set = dbook_set - cover_set

print "-----------------------------------"
print "               EPUBS               "
print " Total = " + str(len(epub_set))
print " Unique = " + str(len(unique_epub_set))
print " E & P = " + str(len(epub_and_pdf_set))
print " E - P = " + str(len(epub_not_pdf_set))
print " E & D = " + str(len(dbook_and_epub_set))
print " E - D = " + str(len(epub_not_dbook_set))
print " E&P&D = " + str(len(common_set))
print "-----------------------------------"
print "               PDFS                "
print " Total = " + str(len(pdf_set))
print " Unique = " + str(len(unique_pdf_set))
print " P & D = " + str(len(pdf_and_dbook_set))
print " P - D = " + str(len(pdf_not_dbook_set))
print " P & E = " + str(len(epub_and_pdf_set))
print " P - E = " + str(len(pdf_not_epub_set))
print "-----------------------------------"
print "             Docbooks              "
print " Total = " + str(len(dbook_set))
print " Unique = " + str(len(unique_dbook_set))
print " D & E = " + str(len(dbook_and_epub_set))
print " D - E = " + str(len(dbook_not_epub_set))
print " D & P = " + str(len(pdf_and_dbook_set))
print " D - P = " + str(len(dbook_not_pdf_set))
print "-----------------------------------"
print "               Covers              "
print " Total  = " + str(len(cover_set))
print " Unique = " + str(len(unique_cover_set))
print " Have: "
print " Epub   = " + str(len(epub_cover_set))
print " PDF    = " + str(len(pdf_cover_set))
print " Dcbk   = " + str(len(dbook_cover_set))
print " Missing: "
print " Epub   = " + str(len(epub_missing_cover_set))
print " PDF    = " + str(len(pdf_missing_cover_set))
print " Dcbk   = " + str(len(dbook_missing_cover_set))


print "-----------------------------------"
#for item in pdf_not_epub_set:
#    print item
