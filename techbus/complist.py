#!/usr/bin/env python
# encoding: utf-8
"""
Created by Matthew Hare March 28th 2013
Copyright (c) 2012 Safari Books Online. All rights reserved.

Interface to Brightcove API
"""

from lxml import etree
import sporklib, time, urllib, urllib2, os

good_list = sporklib.get_query_list('good.txt')
missing_list = sporklib.get_query_list('missing.txt')

for item in missing_list:
    if item in good_list:
        print item
