#!/usr/bin/env python

import os, filecmp, shutil, time
import sporklib

BASE_DIR = "/home/content/uploaded/incoming"
EPUB_DIR = "/home/content/uploaded/epubs"
PDF_DIR = "/home/content/uploaded/pdfs"

ignore_dirs = []
ignore_dirs.append(os.path.join(BASE_DIR,'only_dbook'))

file_FPID_list , file_dict = sporklib.get_fpid_list(BASE_DIR,ignore_dirs)
epub_FPID_list , epub_dict = sporklib.get_fpid_list(EPUB_DIR,ignore_dirs)
pdf_FPID_list , pdf_dict = sporklib.get_fpid_list(PDF_DIR,ignore_dirs)

doc_set = set(file_FPID_list)
epub_set = set(epub_FPID_list)
pdf_set = set(pdf_FPID_list)

in_doc_not_epub_set = doc_set - epub_set
in_doc_not_pdf_set = doc_set - pdf_set
#unique_set = in_doc_not_epub_set - pdf_set
unique_set = in_doc_not_pdf_set - epub_set

in_doc_and_epub_set = doc_set & epub_set
in_doc_and_pdf_set = doc_set & pdf_set
in_all_set = in_doc_and_epub_set & pdf_set

in_doc_and_epub_only_set = in_doc_and_epub_set - in_all_set
in_doc_and_pdf_only_set = in_doc_and_pdf_set - in_all_set

for fpid in in_all_set:
    file_name = fpid + '.pdf'
    file1 = "ERROR1a"
    file2 = "ERROR1b"

    if os.path.exists(os.path.join(BASE_DIR,file_name)):
        file1 = os.path.join(BASE_DIR,file_name)

    if os.path.exists(os.path.join(PDF_DIR,file_name)):
        file2 = os.path.join(PDF_DIR,file_name)
    elif os.path.exists(os.path.join(PDF_DIR,'goodfiles',file_name)):
        file2 = os.path.join(PDF_DIR,'goodfiles',file_name)
    elif os.path.exists(os.path.join(PDF_DIR,'badfiles',file_name)):
        file2 = os.path.join(PDF_DIR,'badfiles',file_name)

    if file1 != "ERROR1a" and file2 != "ERROR1b":
        if filecmp.cmp(file1,file2):
            file3 = os.path.join('/home/content/uploaded/duplicates',file_name)
            print "Moving Dup1 " + file1 + " to " + file3
            #shutil.move(file1,file3)
        else:
            ftime1 = os.path.getmtime(file1)
            ftime2 = os.path.getmtime(file2)
            
            if ftime1 > ftime2:
                file3 = file2
                print "Moving New1 " + file1 + " to " + file3
                #shutil.move(file1,file3)
            else:
                file3 = os.path.join('/home/content/uploaded/oldbooks',file_name)
                print "Moving Old1 " + file1 + " to " + file3
                #shutil.move(file1,file3)
    else:
        print file1
        print file2

for fpid in in_doc_and_pdf_only_set:
    file_name = fpid + '.pdf'
    file1 = "ERROR2a"
    file2 = "ERROR2b"

    if os.path.exists(os.path.join(BASE_DIR,file_name)):
        file1 = os.path.join(BASE_DIR,file_name)

    if os.path.exists(os.path.join(PDF_DIR,file_name)):
        file2 = os.path.join(PDF_DIR,file_name)
    elif os.path.exists(os.path.join(PDF_DIR,'goodfiles',file_name)):
        file2 = os.path.join(PDF_DIR,'goodfiles',file_name)
    elif os.path.exists(os.path.join(PDF_DIR,'badfiles',file_name)):
        file2 = os.path.join(PDF_DIR,'badfiles',file_name)

    if file1 != "ERROR2a" and file2 != "ERROR2b":
        if filecmp.cmp(file1,file2):
            file3 = os.path.join('/home/content/uploaded/duplicates',file_name)
            print "Moving Dup2 " + file1 + " to " + file3
            #shutil.move(file1,file3)
        else:
            ftime1 = os.path.getmtime(file1)
            ftime2 = os.path.getmtime(file2)
            
            if ftime1 > ftime2:
                file3 = file2
                print "Moving New2 " + file1 + " to " + file3
                #shutil.move(file1,file3)
            else:
                file3 = os.path.join('/home/content/uploaded/oldbooks',file_name)
                print "Moving Old2 " + file1 + " to " + file3
                #shutil.move(file1,file3)
    else:
        print file1
        print file2

for fpid in in_doc_and_epub_only_set:
    file_name = fpid + '.pdf'
    file1 = "ERROR3a"
    file2 = "ERROR3b"

    if os.path.exists(os.path.join(BASE_DIR,file_name)):
        file1 = os.path.join(BASE_DIR,file_name)

    if file1 != "ERROR3a":
        file2 = os.path.join(PDF_DIR,file_name)
        print "Moving New3 " + file1 + " to " + file2
        #shutil.move(file1,file2)
    else:
        print file1

for fpid in unique_set:
    file_name = fpid + '.pdf'
    file1 = "ERROR4a"
    file2 = "ERROR4b"

    if os.path.exists(os.path.join(BASE_DIR,file_name)):
        file1 = os.path.join(BASE_DIR,file_name)

    if file1 != "ERROR4a":
        file2 = os.path.join(PDF_DIR,file_name)
        print "Moving New4 " + file1 + " to " + file2
        #shutil.move(file1,file2)
    else:
        print file1

print "Total Incoming " + str(len(doc_set))
print "Total Epubs " + str(len(epub_set))
print "Total PDFS " + str(len(pdf_set))
print "Only Incoming " + str(len(unique_set))
print "Incoming and Epubs " + str(len(in_doc_and_epub_only_set))
print "Incoming and PDFs " + str(len(in_doc_and_pdf_only_set))
print "Common to all " + str(len(in_all_set))


