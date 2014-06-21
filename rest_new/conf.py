#-*- coding:utf-8 -*-

#conf for rest api

MONGO_HOST = '112.124.1.3'
MONGO_PORT = 27017

#mongo db & collection
MONGO_DB = 'amazon_speedata'
MONGO_USER = 'speedata'
MONGO_PWD = '605605'

MONGO_COL = 'commodity'

#api conf
ITEM_PERPAGE = 20

#mobile conf
CATEGORY_DICT = {'office': ['Office Products>Office Furniture & Lighting>Chairs & Sofas>Desk Chairs', 
                            'Office Products>Office Furniture & Lighting>Desks & Workstations'], 
                 'dog': ['Pet Supplies>Dogs'], 
                 'wig': ['Beauty>Hair Care>Styling Products>Hair Extensions & Wigs'], 
                 'dress': ['Clothing & Accessories>Women>Dresses>Special Occasion'], 
                 'skirt': ['Clothing & Accessories>Women>Skirts'], 
                 'bag': ['Shoes>Handbags>Evening Bags']}