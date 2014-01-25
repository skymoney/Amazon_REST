#-*- coding:utf-8 -*-
from flask import Flask, request, url_for, redirect

import simplejson as json
import mongo_util
from mongo_util import ComplexEncoder
import conf

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Amazon REST API"


@app.route('/api/commodity/', methods=['GET'])
def get_all_category():
    category_name = request.args.get('category', '').replace('$', '&')

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

        return json.dumps(map(lambda x:x, com_cursor), cls=ComplexEncoder)

    com_col = mongo_util.get_commodity_col()

    all_category = com_col.distinct('category')

    return json.dumps(map(lambda x: {'name': '>'.join(x)},
                      all_category), cls=ComplexEncoder)

@app.route('/api/commodity/field', methods=['GET'])
def get_available_field():
    '''
            获取可以过滤查询的field
    '''
    return json.dumps(conf.FIELDS)


@app.route('/api/commodity/<asin>', methods=['GET'])
def get_commodity_info(asin):
    '''
            获取指定ASIN的商品信息
    '''
    query_field = mongo_util.generate_query(eval(request.args.get('field', '[]')))
    
    com_col = mongo_util.get_commodity_col()

    asin_info = com_col.find_one({'ASIN': asin},
                                 query_field)

    return json.dumps(asin_info, cls=ComplexEncoder)

@app.route('/api/custom/', methods=['GET'])
def custom_query():
    '''
            自定义查询，可以查找需要的数据，需要对MongoDB的查询熟悉
    '''
    if request.args.get('query', '') or request.args.get('ret', ''):
        com_col = mongo_util.get_commodity_col()
        
        #skip = int(request.args.get('skip', '0'))
        query = request.args.get('query', {})
        ret = request.args.get('ret', {})
        
        all_query_cursor = com_col.find(query,ret).batch_size(1000)
        return json.dumps(map(lambda x:x, all_query_cursor), 
                          cls=ComplexEncoder)
    else:
        return redirect('/api/commodity/', code=302)


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
