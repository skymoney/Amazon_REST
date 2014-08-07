#-*- coding:utf-8 -*-

##########################
#
# Simple demo for auth
#
# Author: Cheng@NJU
# Date：2014/08/04
#########################

import urllib2  #you can also use requests
import requests
import base64

url = 'http://112.124.1.3:8020'

username = ''
password = ''

token = ''

def access_by_namepwd():
    '''
    access by username and password
    '''
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

def access_by_token():
    '''
    access by token and use requests to get data
    '''
    token = ''    
    url = 'http://localhost:8020'
    
    res = requests.get(url, auth=(token, ''))
    
    if res.ok:
        print res.text
    else:
        print 'error'

if __name__ == '__main__':
    access_by_namepwd()
    access_by_token()