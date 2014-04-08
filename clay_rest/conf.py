#-*- coding:utf-8-*-

#Mongo Global Conf
MONGO_HOST = '112.124.1.3'
MONGO_PORT = 27017

#MONGO Commodity conf
MONGO_COM_DB = 'amazon_speedata'
MONGO_COM_USER = 'speedata'
MONGO_COM_PWD = '605605'
MONGO_COM_COLLECTION = 'commodity'

#MONGO Auth conf
MONGO_AUTH_DB = 'e_bus_account'
MONGO_AUTH_USER = 'root'
MONGO_AUTH_PWD = '605605'
MONGO_AUTH_COLLECTION = 'ws_token'

#Data conf
FIELDS = ['ASIN', 'productInfo', 'review', 'seller', 'offer', 'stats_info']

ITEM_PER_PAGE = 20