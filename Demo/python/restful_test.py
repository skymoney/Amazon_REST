#-*-coding:utf-8-*-
import httplib   
      
def request_restful(token, params): 
    #params是传递的参数
    param_str = '?'
    for (key, value) in params.items():
        param_str = param_str + key + '=' + value + '?'
    param_str = param_str[:-1]

    #auth就是登录认证的key 
    auth = token
    #将认证和请求格式信息放入请求头中
    headers = {"Authorization": "Basic "+ auth, "Content-Type": "application/json"}   
#   #建立连接   
    conn = httplib.HTTPConnection('112.124.1.3','5000')
    #发送请求   
    conn.request('GET','/commodity'+param_str, None, headers)
    response = conn.getresponse()   
    #print response.status  
#     file = open('test.txt', 'w')
#     file.write(response.read())
    print response.read()
    
if __name__ == '__main__':
	#通过给定ASIN码来访问对应的商品
    params = {'where': 'ASIN==B00AC8SHDW'}
    token = 'YjA1NTRkMzdhYjNjYWRmM2VlMDU0ZThmNTE4ZjNiMmI6'
    request_restful(token, params)
