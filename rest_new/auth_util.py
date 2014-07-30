#-*- coding:utf-8 -*-

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from hashlib import md5
import mongo_util
import settings, conf

def generate_serializer():
    s = Serializer(settings.APP_KEY)
    return s

def generate_token(uername, password):
    s = generate_serializer()
    return s.dumps({'username': username,  
                    'password': password})

def check_auth(username, password):
    '''
    check by username:password or token given to user
    '''
    db = mongo_util.get_auth_db()
    try:
        s = generate_serializer()
        auth_data = s.loads(username)
        if db[conf.MONGO_AUTH_COL].find({'username': auth_data['username']}).count() > 0:
            return True
    except:
        if db[conf.MONGO_AUTH_COL].find({'username': username, \
                                          'password': md5(password).hexdigest()}).count() > 0:
            return True
    return False
    