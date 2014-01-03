#-*- coding:utf-8 -*-

from eve import Eve

from eve.auth import TokenAuth

import pymongo

import mongo_conf as mc

class AmazonToken(TokenAuth):
	#custom token auth for access
	def check_auth(self, token, allowed_roles, resource, method):
		print token
		return self.get_token_col().find_one({'token': token})

	def get_token_col(self):
		con = pymongo.Connection(mc.MONGO_HOST, mc.MONGO_PORT)
		db = con[mc.MONGO_TOKEN_DB]
		try:
			db.authenticate(mc.MONGO_TOKEN_USER,
				mc.MONGO_TOKEN_PWD)
			return db[mc.MONGO_TOKEN_COL]
		except:
			return None

if __name__ == '__main__':
	app = Eve(auth=AmazonToken)
	app.run()
