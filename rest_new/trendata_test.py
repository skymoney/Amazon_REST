#-*- coding:utf-8 -*-

import brand_seller_api

'''
brand_set = brand_seller_api.brand_mobile_field('wig')


for key in brand_set:
    print key.encode('utf-8'), brand_set[key]


final_data = sorted(brand_set.items(), key=lambda x:x[1]['review_count'], reverse=True)[:10]
for data in final_data:
    print data
'''

brand_info = brand_seller_api.brand_info('lilu')

print brand_info