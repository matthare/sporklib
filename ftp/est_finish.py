#!/usr/bin/env python
# encoding: utf-8

import time, subprocess

def flines(file_name):
    lcounter = 0
    f = open(file_name, 'r')
    for line in f:
        lcounter += 1
    f.close()
    return lcounter

def run(cmd):
   call = ["/bin/bash", "-c", cmd]
   output = ''
   try:
      output = subprocess.check_output(call,stderr=subprocess.STDOUT)
      return output   
   except subprocess.CalledProcessError as file_error:
      return file_error.output

def calculate_time(asset):
    if asset == 'epub':
        proc = 'mtgetfiles'
        file1 = './fpid.list'
        file2 = './skipids.txt'
    elif asset == 'pdf':
        proc = 'mtgetpdfs'
        file1 = './fpidpdf.list'
        file2 = './skippdfids.txt'
    elif asset == 'cover':
        proc = 'mtgetcovers'
        file1 = './fpidcover.list'
        file2 = './skipcoverids.txt'
    else:
        return "bogus"
    
    output = run("ps x | grep " + proc)
    output2 = output.split('\n')

    ptime = None
    for line in output2:
        if 'grep' not in line:
            if proc in line:
                words = line.split(' ')
                for word in words:
                    if ':' in word:
                        minutes, seconds = word.split(':')
                        ptime = int(minutes)*60 + int(seconds)

    if ptime == None:
        return proc + " not running"

    total = flines(file1)
    finished = flines(file2)

    total_time = ptime*total/finished
    remaining_time = total_time - ptime
    
    the_time = time.time() + ptime + 3*60*60
    return time.ctime(the_time)



print "Epubs will be done DLing on " + calculate_time('epub')
print "PDFs will be done DLing on " + calculate_time('pdf')
print "Covers will be done DLing on " + calculate_time('cover')


