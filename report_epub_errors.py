#!/usr/bin/env python

import os, filecmp, shutil, time, operator

# open the file from CLassic and read in the FPIDs
# remove none FPID chars
#f = open('/home/content/uploaded/epubcheck-3.0/error_reject.log', 'r')
f = open('/home/content/uploaded/epubcheck-3.0/error_accept.log', 'r')

error_dict = {}
error_dict2 = {}
file_list = []
image_list = []
font_list = []

mycounter = 0
for line in f:
    if 'ERROR:' in line:
        error = line.split(':')
        file_name = error[1].split('/')[7]

        it = 2
        error_id = []
        while len(error_id) < 2:
            error_str = error[it]
            if error_str[0] == ' ':
                error_str = error_str[1:]
            error_id = error_str.split(' ')
            it += 1


        key = "{} {}".format(error_id[0],error_id[1])
            
        if 'file' in error_id and 'appear' in error_id:
            key = 'tfXdnatbotX'
            key_str = 'The file X does not appear to be of type X'
        if 'assertion' in error_id and 'failed' in error_id:
            key = 'assfail'
            key_str = 'assertion failed The X attribute does not have a unique value'
        if 'duplicate' in error_id and 'resource' in error_id:
            key = 'drX'
            key_str = 'duplicate resource X'
        if 'fragment' in error_id and 'identifier' in error_id:
            key = 'fiindiX'
            key_str = 'fragment identifier is not defined in X'
        if 'value' in error_id and 'attribute' in error_id:
            key = 'voaXii'
            key_str = 'value of attribute X is invalid; must be an XML name without colons'
        if 'image' in error_id and 'resource' in error_id:
            key = 'nsirX'
            key_str = 'non-standard image resource X'
        if 'Guide' in error_id and 'reference' in error_id:
            key = 'grtaiinacdX'
            key_str = 'Guide reference to an item that is not a Content Document X'
        if 'date' in error_id and 'value' in error_id:
            key = 'dvXisvaph'
            key_str = 'date value X is not valid as per http'
        if 'spine' in error_id and 'contains' in error_id:
            key = 'scmrttmiwiX'
            key_str = 'spine contains multiple references to the manifest item with id X'
        if 'File' in error_id and 'listed' in error_id:
            key = 'flireigwndiom'
            key_str = 'File listed in reference element in guide was not declared in OPF manifest'
        if 'attribute' in error_id and 'expected' in error_id:
            key = 'aXnaheaX'
            key_str = 'attribute X not allowed here; expected attribute X'
        if 'could' in error_id and 'parse' in error_id:
            key = 'cnpXdi'
            key_str = 'could not parse X duplicate id'
        if 'Only' in error_id and 'encodings' in error_id:
            key = 'ou8au16aa'
            key_str = 'Only UTF-8 and UTF-16 encodings are allowed, detected ISO-8859-1'
        if 'Obsolete' in error_id and 'irregular' in error_id:
            key = 'ooids'
            key_str = 'Obsolete or irregular DOCTYPE statement. The DOCTYPE can be removed.'
        if 'Length' in error_id and 'filename' in error_id:
            key = 'lotffiamb8'
            key_str = 'Length of the first filename in archive must be 8, but was X'
        if 'toc' in error_id and 'attribute' in error_id:
            key = 'tarrwnmt'
            key_str = 'toc attribute references resource with non-NCX mime type; X is expected'
        if 'External' in error_id and 'DTD' in error_id:
            key = 'edeana'
            key_str = 'External DTD entities are not allowed. Remove the DOCTYPE'
        if 'element' in error_id and 'incomplete;' in error_id:
            key = 'eXimreX'
            key_str = 'element X incomplete; missing required element X'
        if 'file' in error_id and 'missing\n' in error_id:
            key = 'XfXim'
            key_str = 'X file X is missing'
        if 'referenced' in error_id and 'resource' in error_id:
            key = 'rXim'
            key_str = 'referenced resource missing in the package'
        if 'resource' in error_id and 'missing\n' in error_id:
            key = 'rXim'
            key_str = 'resource X is missing'
        if 'role' in error_id and 'value' in error_id:
            key = 'rvXinv'
            key_str = 'role value X is not valid'
        if 'element' in error_id and 'missing' in error_id:
            key = 'eXmraX'
            key_str = 'element X missing required attribute X'
        if 'element' in error_id and 'expected' in error_id:
            key = 'eXnah'
            key_str = 'element X not allowed here; expected the element end-tag, text or element X, X,...'
        if 'Entity' in error_id and 'undeclared\n' in error_id:
            key = 'eXiu'
            key_str = 'Entity X is undeclared'
        if 'entity' in error_id and 'declared.\n' in error_id:
            key = 'eXiu'
            key_str = 'The entity X was referenced, but not declared.'
        if 'remote' in error_id and 'resource' in error_id:
            key = 'rrrnarmbpito'
            key_str = 'remote resource reference not allowed; resource must be placed in the OCF'
        if 'Mimetype' in error_id and 'contains' in error_id:
            key = 'mfscots'
            key_str = 'Mimetype contains wrong type (application/epub+zip expected)'
        if 'Mimetype' in error_id and 'file' in error_id:
            key = 'mfscots'
            key_str = 'Mimetype file should contain only the string "application/epub+zip"'
        if 'unique-identifier' in error_id and 'attribute' in error_id:
            key = 'uiaipemraeidi'
            key_str = 'unique-identifier attribute in package element must reference an existing identifier element id'
        if 'Python' in error_id and 'Eggs' in error_id:
            key = 'oaoopapeig'
            key_str = 'OEBPS/Architectural Overview of pkg_resources and Python Eggs in General'


    
        elist = []
        elist = error_dict.setdefault(key,elist)
        _= error_dict2.setdefault(key,key_str)
        if file_name not in elist:
            elist.append(file_name)
        error_dict[key] = elist

f.close()
error_tup = []
for key in error_dict:
    error_tup.append((key, len(error_dict[key])))

for item in sorted(error_tup, key=lambda tup: tup[1], reverse=True):
    print "error type: {:15} {:5} {}".format(item[0],item[1],error_dict2[item[0]])
  

