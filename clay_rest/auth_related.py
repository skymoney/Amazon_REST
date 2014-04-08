#-*- coding: utf-8 -*-

###############################################
#
# Auth Related, including generating account.
#
# Author: Cheng@NJU
# Date: 2014/03/02
###############################################

import base64

import mongo_util

def generate_auth(username, password):
    auth_col = mongo_util.get_auth_col()
    auth_col.insert({'username': username, 'password': password})

if __name__ == '__main__':
    generate_auth('test', 'test')