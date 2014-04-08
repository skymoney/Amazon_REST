#-*- coding:utf-8 -*-

import mongo_util

def check_auth(username):
    auth_col = mongo_util.get_auth_col()    
    data = auth_col.find_one({'username': username})
    
    if data:
        return data['password']
    return None