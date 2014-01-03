#-*- coding:utf-8 -*-

import os
import mongo_conf

SERVER_NAME = '127.0.0.1:5000'

MONGO_HOST = mongo_conf.MONGO_HOST
MONGO_PORT = mongo_conf.MONGO_PORT
MONGO_USERNAME = mongo_conf.MONGO_USERNAME
MONGO_PASSWORD = mongo_conf.MONGO_DA
MONGO_DBNAME = 'amazon_speedata'

RESOURCE_METHODS = ['GET']

ITEM_METHODS = ['GET']

commodity = {
	'item_title':'commodity',

	'additional_lookup': {
		'url': 'regex("[\w|\d]+")',
		'field': 'ASIN'
	},

	'schema': {
		'ASIN':{
			'type': 'String',
			'required': True,
			'unique': True,
		},
		'productInfo': {
			'type': 'list',
		},
		'offer': {
			'type': 'list',
		},
		'review': {
			'type': 'list',
		},
	},
}

DOMAIN = {
	'commodity':commodity,
}

ETAG = None
LINK = None
