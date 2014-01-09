#-*- coding:utf-8 -*-
'''
Created on 2014-1-9

@author: cheng
'''

def generate_query(field=[]):
    print field
    query = dict(zip(field, 
                     [1]*len(field)))
    
    query['_id'] = 0
    print query
    return query
    
