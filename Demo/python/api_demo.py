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
        s = requests.get(url)

def get_entrance():
    username = 'mg1332011@software.nju.edu.cn'
    passwd = '123456'
    t = Trendata(username=username, passwd = passwd)

if __name__ == '__main__':
    pass