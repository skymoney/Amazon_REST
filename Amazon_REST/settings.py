#-*- coding:utf-8 -*-

import os
import mongo_conf

SERVER_NAME = '127.0.0.1:5000'

MONGO_HOST = mongo_conf.MONGO_HOST
MONGO_PORT = mongo_conf.MONGO_PORT
MONGO_USERNAME = mongo_conf.MONGO_DATA_USER
MONGO_PASSWORD = mongo_conf.MONGO_DATA_PWD
MONGO_DBNAME = mongo_conf.MONGO_DATA_DB

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
		'stats_info': {
			'type': 'Dict',
		},
	},
}

category = {
	'item_title': 'category',

	'additional_lookup': {
		'url': 'regex("[\w]+")',
		'field': 'id',
	},

	'schema': {
		'id': {
			'type': 'String',
			'required': True,
			'unique': True,
		},
		'level': {
			'type': 'Int',
		},
		'name': {
			'type': 'String',
		},
		'pid': {
			'type': 'list',
		},
		'product_set': {
			'type': 'list',
		},
		'stats_info': {
			'type': 'Dict'
		},
	}
}

DOMAIN = {
	'commodity': commodity,
	'category': category,
}
