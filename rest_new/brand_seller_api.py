#-*- coding:utf-8 -*-

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
        