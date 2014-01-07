Amazon_REST
===========

针对 爬取到的 Amazon数据提供的REST API。

API采用Python Eve完成。

由于Eve的一些访问问题，采用 Django REST重新实现访问框架
提供对Amazon商品信息的访问。

目前提供的接口：

1, api/commodity/
  获得商品的所有分类，返回分类名列表
  
  [{'name':'A>B>C', 'count': 600},
   {'name':'D>E>F', 'count': 600}]

2, api/commodity/?category_name=A>B>C
  返回指定Category的商品，默认返回第一页集合，共20条，
  如果需要多页的话加上参数 page=n即 &page=n


3, api/commodity/ASDFSDSD/
  获得某一个指定asin的商品

注：如果需要特定的数据，可以加上参数 field=['filedA','filedB']
  这样获得数据的响应会相对较短，例如只需要商品的review信息
  api/commodity/SADFSFSF/?field=['review']
  对于2条也是通用的
   api/commodity/?category_name=A>B>C&field=['review']

4, api/commodity/field
  查看可用的field
  
