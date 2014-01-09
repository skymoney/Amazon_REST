#-*- coding:utf-8 -*-
# Create your views here.

import re

from django.views.decorators.csrf import csrf_exempt
from global_util.ws_conf import JSONResponse

from global_util.ws_conf import get_mongo_db
from global_util.ws_conf import FIELDS, ITEMS_PER_PAGE

import time

import com_util as cu

@csrf_exempt
def get_single_commodity(request, asin):
    '''
    获取单条商品记录，根据指定的filed返回对应信息，默认全部返回
    @param asin: 对应的ASIN
    '''
    db = get_mongo_db()
    
    query_field = cu.generate_query(eval(request.GET.get('field', '[]')))
    
    single_data = db.commodity.find_one({'ASIN': asin},
                                        query_field)    
    
    del db    
    return JSONResponse(single_data)

@csrf_exempt
def get_all_categories(request):
    import time
    '''
    get all categories in commodity
    @return: list of categories
    '''
    db = get_mongo_db()
    
    if request.GET.get('category_name', None):
        '''
        Get products given category name
        '''
        
        query_field = cu.generate_query(eval(request.GET.get('field', '[]')))
        category_set = re.sub(r'\$','&',request.GET.get('category_name')).split('>')
        print request.GET.get('category_name')
        page = int(request.GET.get('page', 1))
        print category_set
        all_data = db.commodity.find({'category':
                                       {'$elemMatch':
                                        {'$all':category_set}}},
                                     query_field).sort('stats_info.review_count',-1).skip(page-1).limit(ITEMS_PER_PAGE)
        
        del db
        return JSONResponse([data for data in all_data])    
    
    '''
    get whole category info
    '''
    all_category_info = db.commodity.distinct('category')
    del db
    return JSONResponse([{'name': '>'.join(cate)} for cate in all_category_info])


@csrf_exempt
def get_ava_filed(request):
    '''
    get all avaiable fields in commodity collection
    read from conf file
    '''
    return JSONResponse(FIELDS.keys())


@csrf_exempt
def custom_query(request):
    '''
    Warning: this may be slow or cause damage to db
         DO NOT use that if unnecessary
    '''
    if request.GET.get('query') or request.GET.get('ret'):
        page = int(request.GET.get('page', '1'))
        
        page = page if page >0 else 1
        
        db = get_mongo_db()
        all_data=db.commodity.find(request.GET.get('query', {}),
                          request.GET.get('ret', {})).sort({'stats_info': -1}).skip(page-1).limit(ITEMS_PER_PAGE)
        
        
        return JSONResponse([data for data in all_data])
    else:
        return get_all_categories(request)
    