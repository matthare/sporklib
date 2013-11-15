import os
import zipfile

#CONTENT_PATH = '/home/mhare/sporklib/uploaded/epubs/clean'
#CONTENT_PATH = '/home/mhare/sporklib/uploaded/epubs/warning'
#CONTENT_PATH = '/home/mhare/sporklib/uploaded/epubs/error/accept'
CONTENT_PATH = '/home/mhare/sporklib/uploaded/epubs/error/reject'

def add_hintfile(epub_path):
    with zipfile.ZipFile(epub_path, 'a') as zippy:
        if 'fromdocbook' not in zippy.namelist():     
            print "Fixing file %s" % dbpath
            zippy.writestr('fromdocbook', '')
        else:
            print "%s already has the hint file" % epub_path


with open('all_epubs_2013-07-11.txt') as fh:
    for fn in fh.readlines():
        fn = fn.strip()

        dbpath = os.path.join(CONTENT_PATH, fn)

        if os.path.isfile(dbpath):
            add_hintfile(dbpath)
        else:
            print "ZOMG!!!: %s" % dbpath
