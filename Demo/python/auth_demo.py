#-*- coding:utf-8 -*-

##########################
#
# Simple demo for auth
#
# Author: Cheng@NJU
# Date：2014/08/04
#########################

import urllib2, base64

url = 'http://localhost:8019'

username = 'mg1332011@software.nju.edu.cn'
password = '123456'

token = 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im1nMTMzMjAxMUBzb2Z0d2FyZS5uanUuZWR1LmNuIiwicGFzc3dvcmQiOiJlMTBhZGMzOTQ5YmE1OWFiYmU1NmUwNTdmMjBmODgzZSJ9.ViwIuxMuvla3qh496LNz8QLFbFcYyF-DnvRcvbvqoYA'

for i in xrange(110):
    request = urllib2.Request(url)
    
    base64String = base64.encodestring('%s:%s'%(token, '')).replace('\n', '')
    
    request.add_header('Authorization', 'Basic %s'%(base64String))
    
    response = urllib2.urlopen(request).read()
    
    print response