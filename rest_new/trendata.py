#-*- coding:utf-8 -*-

import re, os

from flask import Flask, jsonify, make_response, request
from flask.ext.httpauth import HTTPBasicAuth

from datetime import datetime

import mongo_util, conf, brand_seller_api

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

@app.route('/mobilefield/<field>', methods=['GET'])
def multi_category_fetch(field):
	#get category by field
	#field means some categories combined
	target_category_set = conf.CATEGORY_DICT.get(field, ['Pet Supplies>Dogs'])
	#category_set = map(lambda x: x.split('>'), target_category_set)
	db = mongo_util.get_mongo_db()
	
	#all_data = db['commodity'].find({'category.0': {'$in': category_set}}).sort('', -1)
	
	top_number = int(request.args.get('topn', 5))
	
	page = int(request.args.get('page', '0'))
	
	all_fields = eval(request.args.get('fields', "['ASIN', 'productInfo.name', 'productInfo.img']"))
	query_fields = dict(zip(all_fields + ['_id'], 
		[1 for i in xrange(len(all_fields))] + [0]))
	
	final_data = []
	#print target_category_set
	for category in target_category_set:
		current_data = db['commodity'].find({'category':{'$elemMatch': 
				{'$all': category.split('>')}}}, query_fields).sort('stats_info.review_count', 
				-1).skip(page*top_number).limit(top_number).batch_size(3000)
		final_data += map(lambda x: x, current_data)
	
	top_n_commodity = sorted(final_data)[:top_number]
	
	return jsonify({'status': 'ok', 
				'data': top_n_commodity})
	
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

#############seller and brand#########################

@app.route('/mobilefield/brand/<field>', methods=['GET'])
def brand_mobile_field(field):
	return jsonify({'status': 'ok', 
				'data': brand_seller_api.brand_mobile_field(field) })

@app.route('/mobilefield/brand/info/<brand_name>', methods=['GET'])
def brand_info(brand_name):
	return jsonify({'status': 'ok', 
				'data': brand_seller_api.brand_info(brand_name) })

@app.route('/mobilefield/seller/<field>', methods=['GET'])
def seller_mobile_field(field):
	return jsonify({'data': 'ok', 
				'data': sorted(brand_seller_api.seller_mobile_field(field), 
							key=lambda x: x['seller_info']['count'], reverse=True)[0: \
								int(request.args.get('topn', '5'))]})

@app.route('/mobilefield/seller/info/<seller_name>', methods=['GET'])
def seller_info(seller_name):
	return jsonify({'data': 'ok', 
				'data': brand_seller_api.seller_info(seller_name)})

#############custom query##########################

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

			custom_cursor = db[conf.MONGO_COL].find(query, ret).skip((page-1)\
			 * conf.ITEM_PERPAGE).limit(conf.ITEM_PERPAGE).batch_size(2000)

			return jsonify({'status': 'ok', 
				'data': map(lambda x: x, custom_cursor)})
		except:
			return jsonify({'status': 'error', 
				'data': 'not valid custom query'})
			
	return jsonify({'status': 'error', 
		'data': 'not valid custom query'})

#########img dispatcher###################
ROOT_DIR = '/mnt/mongo/ImageData/'

ACCESS_DIR = 'http://112.124.1.3/ImageData/'

@app.route('/img/asin/<asin>', methods=['GET'])
def dispatch_by_asin(asin):
	#url http://xxxx?type=stats&time=?
	db = mongo_util.get_mongo_db()

	target_data = db['commodity'].find_one({'ASIN': asin}, {'category': 1, 'productInfo.img': 1})

	if target_data and target_data['category']:
		category = target_data['category'][0]

		img_dir = ROOT_DIR + '/'.join(category) + '/' + asin

		all_target_files = os.listdir(img_dir)
		
		#filter and get newest img of all types
		all_types = list(set(map(lambda x: x.split('-')[0], all_target_files)))
		
		if request.args.get('filter', '') != 'all':
			filter_img_files = map(lambda type: sorted(filter(lambda x: re.search(r'^'+ type +'.*', x), all_target_files))[-1], all_types)
		else:
			filter_img_files = all_target_files
			
		all_access_imgs = map(lambda x: 
			{'path': ACCESS_DIR + '/'.join(category) + '/' + asin + '/' + x}, 
			filter_img_files)
		
		asin_url = ''
		
		if re.search(r'^http:.*', target_data['productInfo'][0]['img']):
			#use amazon url
			asin_url = target_data['productInfo'][0]['img']
		elif re.search(r'^/mnt/.*', target_data['productInfo'][0]['img']):
			#/mnt/
			asin_url = ACCESS_DIR + '/'.join(target_data['productInfo'][0]['img'].split('/')[2:])
		else:
			pass
			
		return jsonify({'status': 'ok', 'data': {'img': asin_url, 'charts': all_access_imgs}})
	
	return jsonify({'status': 'error', 'data': 'target data not exists'})

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