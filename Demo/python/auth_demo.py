#-*- coding:utf-8 -*-

##########################
#
# Simple demo for auth
#
# Author: Cheng@NJU
# Date：2014/08/04
#########################

import urllib2, base64
import requests

url = 'http://112.124.1.3:8020'
url = 'http://localhost:8019'

username = ''
password = ''

token = ''
for i in xrange(110):
    request = urllib2.Request(url)
     
    base64String = base64.encodestring('%s:%s'%(token, '')).replace('\n', '')
        
    request.add_header('Authorization', 'Basic %s'%(base64String))
    try:
        response = urllib2.urlopen(request)
        print response.code
    except:
        print 'error: ', urllib2.urlopen(request).code