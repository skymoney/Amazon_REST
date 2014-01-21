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