#-*- coding:utf-8 -*-

from hashlib import md5
import conf, mongo_util

def brand_mobile_field(field, **kwargs):
    target_category_set = conf.CATEGORY_DICT.get(field, ['Pet Supplies>Dogs'])
    
    db = mongo_util.get_mongo_db()
    limit = kwargs.get('limit', 10)
    final_data = []
    brand_set = {}
    for category in target_category_set:
        cur_data = db.commodity.find({'category.0': category.split('>')}, 
                                     {'productInfo': 1, 
                                      'offer': 1, 
                                      'ASIN': 1, 
                                      'stats_info': 1}).batch_size(3000)
        final_data += map(lambda x: x, cur_data)
    
    for data in final_data:
        if data['productInfo'][0].has_key('brand'):
            try:
                if brand_set.has_key(data['productInfo'][0]['brand']['name']):
                    brand_set[data['productInfo'][0]['brand']['name']]['count'] += 1
                    brand_set[data['productInfo'][0]['brand']['name']]['review_count'] += \
                        data['stats_info']['review_count']
                else:
                    brand_set[data['productInfo'][0]['brand']['name']] = {}
                    brand_set[data['productInfo'][0]['brand']['name']]['count'] = 1
                    brand_set[data['productInfo'][0]['brand']['name']]['review_count'] = \
                        data['stats_info']['review_count']
            except:
                pass
                #brand_set[data['productInfo'][0]['brand']['name']]['high_price'] = ''
                
    
    return brand_set

def brand_info(brand_name):
    db = mongo_util.get_mongo_db()
    
    brand_info = map(lambda x: x, db['brand'].find({'name': brand_name}, {'_id': 0}))
    
    return brand_info[0] if brand_info else {}

def seller_mobile_field(field, **kwargs):
    target_category_set = conf.CATEGORY_DICT.get(field, ['Pet Supplies>Dogs'])
    
    db = mongo_util.get_mongo_db()
    total_data = [] 
    
    for category in target_category_set:
        cur_data = db['commodity'].find({'category.0': category.split('>')}, 
                                        {'seller': 1, 
                                         'ASIN': 1}).batch_size(3000)
        total_data += map(lambda x: x, cur_data)
    
    seller_set = {}
    for data in total_data:        
        if data['seller']:
            for time_seller in data['seller']:
                for single_seller in time_seller['seller']:
                    try:                   
                        if single_seller.has_key('link') and seller_set.has_key(md5(single_seller['link']).digest()):
                            seller_set[md5(single_seller['link']).digest()]['count'] += 1
                            if single_seller['name'] != 'Null':
                                seller_set[md5(single_seller['link']).digest()]['name']= \
                                    single_seller['name']
                        elif single_seller.has_key('link'):
                            #has no key
                            seller_set[md5(single_seller['link']).digest()]={'count': 1, 
                                'name': single_seller['name']}                            
                        elif single_seller['name'] == 'Amazon' and seller_set.has_key(md5('http://www.amazon.com').digest()):
                            #Amazon Self
                            seller_set[md5('http://www.amazon.com').digest()]['count'] += 1                            
                        else:
                            seller_set[md5('http://www.amazon.com').digest()]={'count': 1, 
                                'name': 'Amazon'}
                    except:
                        pass
    return filter(lambda x: x['name'] != 'Amazon' and x['name'] is not None, 
                  map(lambda x: {'name': x[1].get('name', ''), 
                        'count': x[1]['count']}, seller_set.items()))

def seller_info(seller_name):
    db = mongo_util.get_mongo_db()
    seller_info = map(lambda x:x ,db['brand'].find({'name': seller_name}, {'_id': 0}))
    
    return seller_info[0] if seller_info else {}
    
        