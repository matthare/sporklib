#!/usr/bin/env python
# encoding: utf-8
"""
Created by Matthew Hare March 28th 2013
Copyright (c) 2012 Safari Books Online. All rights reserved.

Interface to Brightcove API
"""

from lxml import etree
import sporklib, time, urllib, urllib2, os

SKIPFILE = 'techbus.skip'
KNOWN_SKIPFILES = set()

if os.path.exists(SKIPFILE):
    for line in open(SKIPFILE, 'r'):
        KNOWN_SKIPFILES.add(line.strip())
# Set this up for appending
skipfile_names = open(SKIPFILE, 'a', 0) # write the skipfiles unbuffered

user_list = []
#user_list.append(('Hiroflare@yahoo.com','my.safaribooksonline.com'))
#user_list.append(('happyflare@yahoo.com','creativeedge.com'))
#user_list.append(('cedge@cedge.com','creativeedge.com'))

#user_list.append(('LeannB2CLibrary@email.com','techbus.safaribooksonline.com'))
#user_list.append(('lksOreillyLib@safaritest.com','techbus.safaribooksonline.com'))
#user_list.append(('lksIBMPressBk@safaritest.com','techbus.safaribooksonline.com'))
#user_list.append(('lksAdobePressBK@email.com','techbus.safaribooksonline.com'))
#user_list.append(('lksmuibk@safaritest.com','techbus.safaribooksonline.com'))

#user_list.append(('AdobePressCE@safaritest.com','creativeedge.com'))
#user_list.append(('LeannAnnCE@safaritest.com','creativeedge.com'))
#user_list.append(('lksmuiCE@safaritest.com','creativeedge.com'))

#user_list.append(('PruFlare@gmail.com','techbus.safaribooksonline.com'))
#user_list.append(('PassFlare@email.com','techbus.safaribooksonline.com'))
#user_list.append(('FrankiFlare@gmail.com','techbus.safaribooksonline.com'))
#user_list.append(('tikiflare@yahoo.com','techbus.safaribooksonline.com'))

#user_list.append(('burtmanb2c10yearly@email.com','my.safaribooksonline.com'))
#user_list.append(('burtmanb2c@email.com','my.safaribooksonline.com'))

#user_list.append(('jefflib@my.com','my.safaribooksonline.com'))
#user_list.append(('jefflib@techbus.com','techbus.safaribooksonline.com'))

#user_list.append(('jvbSL123@oreilly.com','my.safaribooksonline.com'))
#user_list.append(('jvbSL@peachpit.com','my.safaribooksonline.com'))
#user_list.append(('jvbSL@techbus.com','techbus.safaribooksonline.com'))
#user_list.append(('jvbSL@proquestcombo.com','techbus.safaribooksonline.com'))

user_list.append(('mhare1@safaritest.com','techbus.safaribooksonline.com'))
user_list.append(('mhare2@safaritest.com','techbus.safaribooksonline.com'))
user_list.append(('mhare3@safaritest.com','techbus.safaribooksonline.com'))
PWORD = 'test123'

query_fpid_list = sporklib.get_query_list('imagesneeded20130404.txt')
for fpid in KNOWN_SKIPFILES:
    query_fpid_list.remove(fpid)

user_iter = 0
counter = 0
for fpid in query_fpid_list:
    USER = user_list[user_iter][0]
    SITE = user_list[user_iter][1]
    user_iter += 1
    if user_iter >= len(user_list):
        user_iter = 0

    request_url = 'http://{}/adminapi?Method=LoginUser&Login={}&Password={}&Method=DownloadZip&FPID={}&source=ipad&Format=xhtml'.format(SITE,USER,PWORD,fpid)
    status_url = 'http://{}/adminapi?Method=LoginUser&Login={}&Password={}&Method=GetUserZipDownloads'.format(SITE,USER,PWORD)
    decrypt_url = 'http://services.safarilab.com:8080/SBOServlets/sbodecrypt'


    counter +=1
    print "Getting {}".format(fpid)
    print request_url
    print status_url
    request_page = etree.parse(request_url)
    time.sleep(5)
    status_page = etree.parse(status_url)
    status = status_page.xpath("/Safari/Context/User/ZipDownloads/ZipDownload/Status/text()")

    while len(status) < 1:
        USER = user_list[user_iter][0]
        SITE = user_list[user_iter][1]
        user_iter += 1
        if user_iter >= len(user_list):
            user_iter = 0
        request_url = 'http://{}/adminapi?Method=LoginUser&Login={}&Password={}&Method=DownloadZip&FPID={}&source=ipad&Format=xhtml'.format(SITE,USER,PWORD,fpid)
        status_url = 'http://{}/adminapi?Method=LoginUser&Login={}&Password={}&Method=GetUserZipDownloads'.format(SITE,USER,PWORD)

        print request_url
        print status_url
        request_page = etree.parse(request_url)
        time.sleep(5)
        status_page = etree.parse(status_url)
        status = status_page.xpath("/Safari/Context/User/ZipDownloads/ZipDownload/Status/text()")

    while status[0] == 'Deleted':
        USER = user_list[user_iter][0]
        SITE = user_list[user_iter][1]
        user_iter += 1
        if user_iter >= len(user_list):
            user_iter = 0
        request_url = 'http://{}/adminapi?Method=LoginUser&Login={}&Password={}&Method=DownloadZip&FPID={}&source=ipad&Format=xhtml'.format(SITE,USER,PWORD,fpid)
        status_url = 'http://{}/adminapi?Method=LoginUser&Login={}&Password={}&Method=GetUserZipDownloads'.format(SITE,USER,PWORD)

        print request_url
        print status_url
        request_page = etree.parse(request_url)
        time.sleep(5)
        status_page = etree.parse(status_url)
        status = status_page.xpath("/Safari/Context/User/ZipDownloads/ZipDownload/Status/text()")

    while status[0] != 'Done':
        print "Not done yet {}".format(status[0])
        time.sleep(5)
        status_page = etree.parse(status_url)
        status = status_page.xpath("/Safari/Context/User/ZipDownloads/ZipDownload/Status/text()")

    login = status_page.xpath("/Safari/Context/User/Login/text()")
    email = status_page.xpath("/Safari/Context/User/Contact/Email/text()")
    session_key = status_page.xpath("/Safari/Results/LoginUser/SessionKey/text()")
    session_id = status_page.xpath("/Safari/Results/LoginUser/SessionId/text()")
    file_name = status_page.xpath("/Safari/Context/User/ZipDownloads/ZipDownload/FileName/text()")[0].replace('/zip/','') 
   
    params = urllib.urlencode({"username": login[0], "login": email[0], "key": session_key[0], "sessionid": session_id[0], "zip": file_name})

    url = decrypt_url + "?" + params
    urllib.urlretrieve(url, file_name.replace('.zip','.tgz'))
    print "{} DLed {}".format(counter,file_name.replace('.zip','.tgz'))
    skipfile_names.write(fpid + "\n")
skipfile_names.close()




