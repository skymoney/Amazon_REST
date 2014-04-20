#-*- coding:utf-8 -*-

import pymongo

import conf

def get_mongo_db():
	con = pymongo.Connection(conf.MONGO_HOST, conf.MONGO_PORT)

	db = con[conf.MONGO_DB]

	try:
		db.authenticate(conf.MONGO_USER, conf.MONGO_PWD)
		return db
	except:
		return None