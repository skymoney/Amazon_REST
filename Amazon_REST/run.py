#-*- coding:utf-8 -*-

from eve import Eve

from eve.auth import TokenAuth, BasicAuth

import pymongo

import mongo_conf as mc


class AmazonToken(TokenAuth):
	#custom token auth for access

	def check_auth(self, token, allowed_roles, resource, method):
		#token_origin = re.search(r'\?[\w]+=[\w]+&?',request.url)
		#token = token_origin[7:len(token_origin-1)]
		#return self.get_token_col().find_one({'token': token})
		#return True
		if token == 'isenju':
			return True
		else:
			return False
		#token_info = self.get_token_col().find_one({'token': token})

		#return True
		'''
		if token:
			return True
		else:
			return False
		'''
	'''
	def authenticate(self):
		re_method = dir(request)
		l=[]
		for m in re_method:
			l.append(m)
		#return '$$'.join(l)+ "%%" + '&&'.join(request.headers.keys())
		return request.url
	'''
	

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
	app = Eve()
	app.run()
