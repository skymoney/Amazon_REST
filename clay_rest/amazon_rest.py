#-*- coding:utf-8 -*-
from flask import Flask, request, url_for, redirect, jsonify, Response
from flask.ext.compress import Compress
from flask.ext.httpauth import HTTPBasicAuth

import simplejson as json
import mongo_util
from mongo_util import ComplexEncoder
import conf
import auth_util

def get_app():
    app = Flask(__name__)
    Compress(app)
    return app

app = get_app()

auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
    return auth_util.check_auth(username)


@app.route('/')
def hello_world():
    return "Amazon REST API"


@app.route('/api/commodity/', methods=['GET'])
def get_all_category():
    category_name = request.args.get('category_name', '').replace('$', '&')

    if category_name:
      	query_field = mongo_util.generate_query(eval(request.args.get('field', '[]')))
        
        try:
            page = int(request.args.get('page', '1'))
        except:
            page = 1
        page = page if page > 0 else 1
        
        #get target collection from mongodb
        com_col = mongo_util.get_commodity_col()
        
        com_cursor = com_col.find(
            {'category': {'$elemMatch': {'$all': category_name.split('>')}}},
            query_field).skip((page - 1) * conf.ITEM_PER_PAGE).limit(conf.ITEM_PER_PAGE).batch_size(500)

        return Response(json.dumps(map(lambda x:x, com_cursor), cls=ComplexEncoder), mimetype='application/json')

    com_col = mongo_util.get_commodity_col()

    all_category = com_col.distinct('category.0')

    return Response(json.dumps(map(lambda x: {'name': '>'.join(x)},
                      all_category), cls=ComplexEncoder), mimetype='application/json')

@app.route('/api/commodity/field/', methods=['GET'])
def get_available_field():
    '''
            获取可以过滤查询的field
    '''
    return jsonify(results = conf.FIELDS)
    #return Resonse(jsonify(conf.FIELDS), mimetype='application/json')


@app.route('/api/commodity/count/', methods=['GET'])
def get_category_count():
    '''获取某一个分类下的所有商品数目'''
    if request.args.get('category_name', ''):
        category = request.args.get('category_name', '').replace('$', '&')
        
        com_col = mongo_util.get_commodity_col()
        
        category_count = com_col.find({'category': 
                                       {'$elemMatch': {'$all': 
                                                       category.split('>')}}}).count()
        return jsonify({'category': category,
                           'count': category_count})
    else:
        return jsonify({'error': 'not valid'})
        

@app.route('/api/commodity/<asin>/', methods=['GET'])
def get_commodity_info(asin):
    '''
            获取指定ASIN的商品信息
    '''
    query_field = mongo_util.generate_query(eval(request.args.get('field', '[]')))
    
    com_col = mongo_util.get_commodity_col()

    asin_info = com_col.find_one({'ASIN': asin},
                                 query_field)
    del com_col
    return Response(json.dumps(asin_info, cls=ComplexEncoder), 
                    mimetype='application/json')

@app.route('/api/custom/', methods=['GET'])
def custom_query():
    '''
            自定义查询，可以查找需要的数据，需要对MongoDB的查询熟悉
    '''
    if request.args.get('query', '') or request.args.get('ret', ''):
        com_col = mongo_util.get_commodity_col()
        #skip = int(request.args.get('skip', '0'))
        query = eval(request.args.get('query', '{}').replace('$', '&'))
        ret = eval(request.args.get('ret', '{}').replace('$', '&'))
        #not return _id for serilization
        ret['_id'] = 0
        all_query_cursor = com_col.find(query,ret).batch_size(5000)
        
        return Response(json.dumps(map(lambda x:x, all_query_cursor), 
                          cls=ComplexEncoder), mimetype='application/json')
    else:
        return redirect('/api/commodity/', code=302)

@app.route('/api/commodity/custom/', methods=['GET'])
def commodity_custom():
    return redirect(url_for('custom_query', **request.args))


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'status': 'error', 'data': 'page not found'})

@app.errorhandler(500)
def server_error(error):
    return jsonify({'status': 'error', 'data': 'server error'})

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
