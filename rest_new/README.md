1, /
    接口列表： 数据接口入口
    接口信息：
        URL： http://112.124.1.3:8020/
        支持格式：JSON
        http请求方式： GET
        DEMO： http://112.124.1.3:8020/
    传递参数：
        无
    返回字段：
      字段    类型        说明
      data    String    返回具体的数据
      status  String    返回状态说明
      timestamp date    时间戳
    
    JSON返回演示
    {
      "data": "Trendata API",
      "status": "ok",
      "time": "Thu, 24 Apr 2014 14:44:33 GMT"
    }
      
    
2, /category/all
    接口列表： 全部数据分类查询
    接口信息：
        Url：http://112.124.1.3:8020/category/all
        支持格式: JSON
        http请求方式： GET
        DEMO：http://112.124.1.3:8020/category/all
    传递参数
        无
    返回字段：
      字段    类型      说明
      data    lits      所有分类说明
      status  String    返回状态说明
    JSON返回演示
    {
    "data": [
      {
        "name": "Baby Products>Diapering>Diaper Bags"
      },
      {
        "name": "Baby Products>Nursery>Bedding"
      }，
      。。。
      ],
    "status": "ok"
    }
      
3, /category/count/<category>
    接口列表： 返回给定分类的统计信息
    接口信息：
        URL： http://112.124.1.3:8020/category/count/<category>
        支持格式： JSON
        HTTP请求方式： GET
        DEMO： hhttp://112.124.1.3:8020/category/count/Beauty>Fragrance>Sets
    传递参数
        无
    返回字段：
      字段    类型        说明
      data    Dict        返回的数据
      status  String      返回状态说明
    
    JSON返回演示：
    {
      "data": {
        "count": 575,
        "name": "Beauty>Fragrance>Sets"
      },
      "status": "ok"
    }

4, /category/<category>
    接口列表： 返回给定分类下的商品信息
    接口信息

5, /fields/

6, /commodity/<asin>

7, /custom/
