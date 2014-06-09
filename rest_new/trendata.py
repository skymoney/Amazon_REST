#-*- coding:utf-8 -*-

from flask import Flask, jsonify, make_response, request
from flask.ext.httpauth import HTTPBasicAuth


from datetime import datetime

import mongo_util, conf

app = Flask(__name__)

def get_app():
	app = Flask(__name__)
	app.config.from_object('settings')
	return app

app = get_app()

def check_pwd(username):
	return None


@app.route('/', methods=['GET'])
def index():
	ret_val = {'status': 'ok', 
		'data': 'Trendata API', 
		'time': datetime.now()}
	return jsonify(ret_val)

@app.route('/category/all', methods=['GET'])
def all_categories():
	'''fetch all categories'''
	db = mongo_util.get_mongo_db()

	all_cate = db[conf.MONGO_COL].distinct('category.0')
	all_cate_info = map(lambda x:{'name': '>'.join(x)}, filter(lambda x: x if x else [], all_cate))

	return jsonify({'status': 'ok', 'data': all_cate_info})

@app.route('/category/count/<category>', methods=['GET'])
def category_commodity(category):
	'''fetch commodity info given category name'''
	db = mongo_util.get_mongo_db()

	category_cursor = db[conf.MONGO_COL].find({'category.0': 
		category.replace('$', '&').split('>')})

	return jsonify({'status': 'ok', 'data': 
		{'name': category.replace('$', '&'), 
		'count': category_cursor.count()}})

@app.route('/category/<category>', methods= ['GET'])
def category_commodity_info(category):
	'''fetch commodity info given category name'''
	db = mongo_util.get_mongo_db()

	category_name = category.replace('$', '&').split('>')

	all_fields = eval(request.args.get('fields', "['ASIN']"))
	query_fields = dict(zip(all_fields + ['_id'], 
		[1 for i in xrange(len(all_fields))] + [0]))

	page = int(request.args.get('page', '1'))

	current_data_cursor = db[conf.MONGO_COL].find({'category.0': category_name}, 
		query_fields).sort('stats_info.review_count', 
		-1).skip((page - 1)*conf.ITEM_PERPAGE).\
		limit(conf.ITEM_PERPAGE).batch_size(2000)

	return jsonify({'status': 'ok', 
			'page': page, 
			'data': map(lambda x: x, current_data_cursor)})

@app.route('/fields/', methods=['GET'])
def field_available():
	'''get all available fields'''
	return jsonify({'status': 'ok', 
		'data': ['ASIN', 'offer', 'review', 'seller', 'productInfo']})

@app.route('/commodity/<asin>/', methods=['GET'])
def single_commodity(asin):
	'''get single commodity info'''
	db =  mongo_util.get_mongo_db()

	all_fields = eval(request.args.get('field', "['ASIN']"))
	query_fields = dict(zip(all_fields + ['_id'], 
			[1 for i in xrange(len(all_fields))] + [0]))

	commodity_info = db[conf.MONGO_COL].find_one({'ASIN': asin}, 
		query_fields)

	return jsonify({'status': 'ok', 'data': commodity_info})

@app.route('/custom/', methods=['GET'])
def custom_query():
	'''custom query for data'''
	if "query" in request.args or "ret" in request.args:
		try:
			query = eval(request.args.get('query', "{}"))
			ret = eval(request.args.get('ret', "{}"))
			ret['_id'] = 0

			db = mongo_util.get_mongo_db()

			page = int(request.args.get('page', '1'))

			custom_cursor = db[conf.MONGO_COL].find(query, ret).skip((page)\
			 * conf.ITEM_PERPAGE).limit(conf.ITEM_PERPAGE).batch_size(2000)

			return jsonify({'status': 'ok', 
				'data': map(lambda x: x, custom_cursor)})
		except:
			return jsonify({'status': 'error', 
				'data': 'not valid custom query'})
			
	return jsonify({'status': 'error', 
		'data': 'not valid custom query'})

#########error handler####################
@app.errorhandler(404)
def not_found_error(error):
	return make_response(jsonify({'status': 'error', 
		'data': 'resource not found'}), 404)

@app.errorhandler(500)
def server_error(error):
	return make_response(jsonify({'status': 'error', 
		'data': 'server error'}), 500)

@app.errorhandler(504)
def bad_gateway(error):
	return make_response(jsonify({'status': 'error', 
		'data': 'bad gateway'}), 504)

@app.errorhandler(502)
def bad_request(error):
	return make_response(jsonify({'status': 'error', 
		'data': 'bad request'}), 502)

#main entrance
if __name__ == '__main__':
	app.debug = False
	app.run(host='0.0.0.0',port=8019)