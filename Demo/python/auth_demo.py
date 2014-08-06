#-*- coding:utf-8 -*-

##########################
#
# Simple demo for auth
#
# Author: Cheng@NJU
# Date：2014/08/04
#########################

import urllib2, base64
import requests  #you can also use requests

url = 'http://112.124.1.3:8020'

username = ''
password = ''

token = ''

request = urllib2.Request(url)

#Use token here, username&password can also be used     
base64String = base64.encodestring('%s:%s'%(token, '')).replace('\n', '')
        
request.add_header('Authorization', 'Basic %s'%(base64String))
try:
    response = urllib2.urlopen(request)
    print response.code  #usually 200
    print response.read()   #response content
except:
    print 'error'