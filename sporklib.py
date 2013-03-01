import os, filecmp, shutil, time

def get_fpid_list(base_dir,ignore_dirs):
    mylist = []
    for dirpath, dirnames, filenames in os.walk(base_dir):
        if dirpath not in ignore_dirs:
            for files in filenames:
                mylist.append(os.path.join(dirpath,files))
    mydict = {}
    for files in mylist:
        fname = os.path.splitext(os.path.split(files)[1])[0]
        fpid, _ = os.path.splitext(fname)
        fmtime = os.path.getmtime(files)
        _= mydict.setdefault(fpid,fmtime)
    myfpid_list = []
    for fpid in mydict:
        lead = fpid[:5]
        if lead.isdigit():
            myfpid_list.append(fpid)
        else:
            print "This file name does not conform to FPID format: " + fpid
    myfpid_list.sort()
    return mylist, myfpid_list, mydict


def get_query_list(file_name = './querylist.txt'): 
    f = open(file_name, 'r')
    fpid_list = []
    for line in f:
        new_line = line.rstrip()
        fpid_list.append(new_line)
    f.close()
    fpid_list.sort()
    return fpid_list
