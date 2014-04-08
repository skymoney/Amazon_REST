#-*- coding:utf-8 -*-

from datetime import datetime,date

import pymongo

import simplejson as json

import conf

class ComplexEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		elif isinstance(obj, date):
			return obj.strftime('%Y-%m-%d %H:%M:%S')
		else:
			return json.JSONEncoder.default(self, obj)

def get_commodity_col():
	con = pymongo.Connection(conf.MONGO_HOST, conf.MONGO_PORT)
	db = con[conf.MONGO_COM_DB]
	try:
		db.authenticate(conf.MONGO_COM_USER, conf.MONGO_COM_PWD)
		return db[conf.MONGO_COM_COLLECTION]
	except:
		return None

def get_auth_col():
	'''get auth data collection'''
	con = pymongo.Connection(conf.MONGO_HOST, conf.MONGO_PORT)
	db = con[conf.MONGO_AUTH_DB]
	try:
		db.authenticate(conf.MONGO_AUTH_USER, conf.MONGO_AUTH_PWD)
		return db[conf.MONGO_AUTH_COLLECTION]
	except:
		return None

def generate_query(field=[]):
    query = dict(zip(field, 
                     [1]*len(field)))    
    query['_id'] = 0
    
    return query