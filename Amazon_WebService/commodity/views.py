#-*- coding:utf-8 -*-
# Create your views here.

from django.views.decorators.csrf import csrf_exempt
from global_util.ws_conf import JSONResponse

from global_util.ws_conf import get_mongo_db
from global_util.ws_conf import FIELDS, ITEMS_PER_PAGE


@csrf_exempt
def get_single_commodity(request, asin):
    '''
    Get single commodity info
    '''
    db = get_mongo_db()
    
    query_field = {'_id': 0}
    
    if request.GET.get('field',[]):
        field=eval(request.GET.get('field'))
        print field
        for f in field:
            query_field[f]=1
    
    single_data = db.commodity.find_one({'ASIN': asin},
                                        query_field)    
    
    del db
    
    return JSONResponse(single_data)

@csrf_exempt
def get_all_categories(request):
    '''
    get all categories in commodity
    @return: list of categories
    '''
    db = get_mongo_db()
    query_field = {'_id': 0}
    
    if request.GET.get('category_name', None):
        '''
        Get products given category name
        '''
        if request.GET.get('field', []):
            field = eval(request.GET.get('field'))
            for f in field:
                query_field[f]=1
        category_set = request.GET.get('category_name').split('>')
        
        page = int(request.GET.get('page', 1))
        
        all_data = db.commodity.find({'category':
                                       {'$elemMatch':
                                        {'$all':category_set}}},
                                     query_field).skip(page-1).limit(ITEMS_PER_PAGE)
        
        all_ret_data = []
        for data in all_data:
            all_ret_data.append(data)
        del db
        return JSONResponse(all_ret_data)    
    
    '''
    get whole category info
    '''
    all_category_info = db.commodity.distinct('category')    
    cate_set = []
    for cate in all_category_info:
        cate_set.append({'name':'>'.join(cate),
                         'count': db.commodity.find({'category':
                                    {'$elemMatch':{'$all':cate}}}).count()})
    
    del db
    return JSONResponse(cate_set)


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
                          request.GET.get('ret', {})).skip(page-1).limit(ITEMS_PER_PAGE)
        
        
        return JSONResponse([data for data in all_data])
    else:
        return get_all_categories(request)
    