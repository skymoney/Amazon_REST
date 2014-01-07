#-*- coding: utf-8 -*-
'''
Created on 2014-1-7

@author: cheng
'''
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

import pymongo

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def get_mongo_db():
    con = pymongo.Connection('112.124.1.3', 27017)
    db = con.amazon_speedata
    try:
        db.authenticate('speedata', '605605')
        return db
    except:
        return None

ITEMS_PER_PAGE = 20

FIELDS = {'ASIN':'1',
          'seller': '1',
          'offer': '1',
          'review': '1',
          'productInfo': '1',
          'stats_info': '1',
          }