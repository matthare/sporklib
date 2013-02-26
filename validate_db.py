#!/usr/bin/env python

from lxml import etree
import zipfile, os

BASE_DIR = "/home/content/uploaded/zips/docbooks/dbs"

ignore_dirs = []
ignore_dirs.append(os.path.join(BASE_DIR,'epubs'))
ignore_dirs.append(os.path.join(BASE_DIR,'pdfs'))
ignore_dirs.append(os.path.join(BASE_DIR,'dbs'))

dir_list = []
file_list = []
path_list = []

for dirpath, dirnames, filenames in os.walk(BASE_DIR):
    if dirpath not in ignore_dirs:
        for dirs in dirnames:
            dir_list.append(dirs)
        for files in filenames:
            file_list.append(files)
            path_list.append(os.path.join(dirpath,files))

zip_pdf = []
true = 0
false = 0
print len(path_list)
counter = 0
for files in path_list:
    counter += 1
    if not counter%100:
        print counter

    try:
        with zipfile.ZipFile(files,'r') as myzip:
            items = myzip.namelist()
            
            for item in items:
                if 'book1.xml' in item:
#                    print item
                    xmlfile = myzip.open(item)
                    
                    dtd = etree.DTD(open('/home/mhare/DocbookSJV/docbookSJV.dtd','rb'))
                    docbook = etree.parse(xmlfile)
                    if dtd.validate(docbook):
                        true += 1
                    else:
                        false += 1
        myzip.close()
    except:
        print "Error " + files
        
print true 
print false
