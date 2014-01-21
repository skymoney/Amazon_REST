#-*- coding;utf-8 -*-
from flask import Flask, request

import simplejson as json
import mongo_util
from mongo_util import ComplexEncoder

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello World!"


@app.route('/api/commodity/', methods=['GET'])
def get_all_category():
    # if request.method == 'GET':
    category_name = request.args.get('category', None)

    if category_name:
      	field = eval(request.args.get('field', '[]'))
       	page = int(request.args.get('page', 1))
        com_col = mongo_util.get_commodity_col()
        com_cursor = com_col.find(
            {'category': {'$elemMatch': {'$all': category_name.split('>')}}}, 
            {'ASIN': 1}).skip(page-1).limit(20)

        return json.dumps(map(lambda x:x['ASIN'], com_cursor))

    com_col = mongo_util.get_commodity_col()

    all_category = com_col.distinct('category')

    return json.dumps(map(lambda x: {'name': '>'.join(x)},
                      all_category), cls=ComplexEncoder)


@app.route('/api/commodity/<asin>', methods=['GET'])
def get_commodity_info(asin):
    com_col = mongo_util.get_commodity_col()

    asin_info = com_col.find_one({'ASIN': asin},
                                 {'_id': 0, 'review': 0})

    return json.dumps(asin_info, cls=ComplexEncoder)

if __name__ == '__main__':
    app.debug = True
    app.run(port=8001)
