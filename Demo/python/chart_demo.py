#-*- coding:utf-8-*-

#######################
# 根据数据简单绘制一些统计图表
#
# Author: Cheng@NJU
#######################

import urllib
import simplejson as json

from datetime import datetime
import matplotlib.pyplot as plt

###
#根据 http://112.124.1.3:8004/api/commodity/B00547HWBE/
# 的信息来进行Demo演示

def get_product_data():
    target_url = 'http://112.124.1.3:8004/api/commodity/B00547HWBE/'
    return json.loads(urllib.urlopen(target_url).read())

def review_hist():
    '''根据评论绘制出评论打分的直方图'''    
    product_data = et_product_data()
    
    star_list = [float(single_review['star'].split()[0]) \
                 for single_review in product_data['review']]
    
    review_hist = plt.hist(star_list, color='grey', align='mid', bins = 5, rwidth=0.5)
    
    #plt.show()
    return review_hist


def price_line():
    '''根据价格绘制出价格走向的折线图'''
    product_data = get_product_data()
    
    price_list=[]
    date_list=[]
    
    for offer in product_data['offer']:
        price_list.append(offer['info'][0]['price'])
        date_list.append(datetime.strptime(offer['info'][0]['timestamp'], 
                                           '%Y-%m-%d %H:%M:%S'))
    
    plt.plot(date_list, price_list, 'o--')
    plt.gcf().autofmt_xdate()
    plt.xlabel('时间')
    plt.ylabel('价格')
    
    plt.show()

def review_time():
    '''根据评论绘制时间增量图'''
    product_data = get_product_data()
    

if __name__ == '__main__':
    #plt.show()
    price_line()