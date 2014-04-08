#-*- coding:utf-8 -*-

import urllib

def test_server_error():
    url = 'http://localhost:5000/api/commodity/B00547HWBE/?field=[27AIN%27]'
    data = eval(urllib.urlopen(url).read())
    if data:
        print 'have data...'
    else:
        print 'not have data...'

if __name__ == '__main__':
    test_server_error()