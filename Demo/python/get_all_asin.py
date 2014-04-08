#-*- coding:utf-8-*-

import urllib

cate = 'Clothing & Accessories>Women>Active'

target_url = 'http://112.124.1.3:8004/api/custom'

query = {'category':{'$elemMatch':{'$all': cate.split('>')}}}
ret = {'ASIN':1, '_id': 0}

quest_data = {'query': query, 'ret': ret}

data = urllib.urlopen('?'.join([target_url, 
                                urllib.urlencode(quest_data)
                                ])).read()

print eval(data)