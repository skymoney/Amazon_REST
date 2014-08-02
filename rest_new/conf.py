#-*- coding:utf-8 -*-

#conf for rest api

MONGO_HOST = '112.124.1.3'
MONGO_PORT = 27017

#mongo db & collection
MONGO_DB = 'amazon_speedata'
MONGO_USER = 'speedata'
MONGO_PWD = '605605'

MONGO_COL = 'commodity'

#mongo auth db & collection
MONGO_AUTH_DB = 'e_bus_account'
MONGO_AUTH_USER = 'root'
MONGO_AUTH_PWD = '605605'

MONGO_AUTH_COL = 'ws_token'

#redis conf
REDIS_HOST = ''
REDIS_PORT = ''

#api conf
ITEM_PERPAGE = 20

#mobile conf
CATEGORY_DICT = {'office': ['Office Products>Office Furniture & Lighting>Chairs & Sofas>Desk Chairs', 
                            'Office Products>Office Furniture & Lighting>Desks & Workstations'], 
                 'dog': ['Pet Supplies>Dogs>Beds & Furniture', 
                         'Pet Supplies>Dogs>Carriers & Travel Products', 
                         'Pet Supplies>Dogs>Feeding & Watering Supplies', 
                         'Pet Supplies>Dogs>Food', 
                         'Pet Supplies>Dogs>Litter & Housebreaking', 
                         'Pet Supplies>Dogs>Memorials',], 
                 'wig': ['Beauty>Hair Care>Styling Products>Hair Extensions & Wigs'], 
                 'dress': ['Clothing & Accessories>Women>Dresses>Special Occasion'], 
                 'skirt': ['Clothing & Accessories>Women>Skirts'], 
                 'bag': ['Shoes>Handbags>Evening Bags']}