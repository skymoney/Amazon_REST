package third_party_rest;

import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.WebResource;
import com.sun.jersey.api.client.filter.HTTPBasicAuthFilter;

public class Amazon_REST_Third {
	public static final String BASE_URL = "http://112.124.1.3:5000/";
	public static final String PRODUCT_URL = BASE_URL + "commodity/";
	
	public static void get_base_resource(){
		//创建一个Client 实例
		Client client = Client.create();
		
		//设置Basic Auth认证
		client.addFilter(new HTTPBasicAuthFilter("username","password"));
		
		//封装请求的资源，包括目标url等
		WebResource wr = client.resource(BASE_URL);
		
		//发送GET请求获取数据
		String response_data = wr.get(String.class);
		
		System.out.println(response_data);		
	}
	
	public static void get_specified_product(String asin){
		//设置同上
		Client client = Client.create();
		client.addFilter(new HTTPBasicAuthFilter("username", "password"));
		
		//设置条件查询
		//具体可以参见http://python-eve.org/features.html#filtering-and-sorting
		String target_asin = "?where=ASIN=="+asin;
		WebResource wr = client.resource(PRODUCT_URL+target_asin);
		
		String response_data = wr.get(String.class);
		
		System.out.println(response_data);
	}
	
	public static void main(String[] args){
		//获取根Url下的内容
		get_base_resource();
		
		//获取指定ASIN码的商品信息
		get_specified_product("B00FAC8TKG");
	}
}
