#-*- coding:utf-8 -*-

########################
#
# API Demo using Python
#
# Author: Cheng@NJU
########################

import requests

class Trendata:
    def __init__(self, username=None, passwd=None, token=None):
        self.username = username
        self.passwd = passwd
        self.token = token
    
    def check_auth(self):
        pass
    
    def get_data(self, url):
        #using HTTP Basic Auth
        if self.username and self.passwd:
            s = requests.get(url, auth=(self.username, self.passwd))
        elif self.token:
            s = requests.get(url, auth=(self.token, ''))
        else:
            return None
        
        return s.text if s.ok else None
        
username = 'mg1332011@software.nju.edu.cn'
passwd = '123456'
t = Trendata(username=username, passwd=passwd)

def get_entrance():
    '''
    test entrance
    '''
    url = 'http://112.124.1.3:8020'
    print t.get_data(url)

def get_commodity_info():
    '''
    get commodity info
    '''
    url = 'http://112.124.1.3:8020/commodity/B000GHVGRI?field=["productInfo", "ASIN"]'
    data = t.get_data(url)  #return data
    
    #convert to json format
    json_data = eval(data) # or json.loads(data)
    
    #print some info
    #to get more, visit http://112.124.1.3:8003/api
    print '商品名为：', json_data['data']['productInfo'][0]['name']
    print '对应ASIN为：', json_data['data']['ASIN']

if __name__ == '__main__':
    #get_entrance()
    get_commodity_info()