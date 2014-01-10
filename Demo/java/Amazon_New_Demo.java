package third_party_rest;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

/**
 *新的Web Service接口Demo
 *仅仅提供了简单的访问演示，更多查询访问参考 
 *   https://github.com/skymoney/Amazon_REST
 *此外，这里只是提供了得到返回的String数据，具体处理还要需要
 *转化成JSON格式数据才能处理，Java中处理JSON的库有很多可以
 *参考，Jackson， json-lib等。 
 */
public class Amazon_New_Demo {
	private static final String BASE_URL = "http://112.124.1.3:8004/api/commodity/";
	
	public static String get_response(String url_name){
		URL url;
		HttpURLConnection conn;
		BufferedReader rd;
		String line;
		String result = "";
		try {
			url = new URL(url_name);
			conn = (HttpURLConnection)url.openConnection();
			conn.setRequestMethod("GET");
			
			//得到返回的结果
			rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
			
			while((line = rd.readLine()) != null){
				result += line;
			}
			
			rd.close();
			
			return result;
		} catch (MalformedURLException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}
	
	/**
	 * 获取所有的Category
	 * */
	public static void get_all_caetgory(){
		System.out.println(get_response(BASE_URL));	
	}
	
	/**
	 * 获取指定分类的商品信息，注意，当filed没有指定时，返回效率较低
	 * 因此尽量只获取需要的数据， Fetch ONLY what you need
	 * */
	public static void get_specified_commodity(){
		//以某一分类为例
		String category_name = "Beauty>Hair Care>Styling Products>Hair Extensions & Wigs";
		//获取ASIN码，多个field通过,分割，如 ["ASIN","productInfo"]
		String field = "[\"ASIN\"]";
		
		//注意，需要将分类中 & 替换成 $，以免参数错误
		String url_name = BASE_URL + "?category_name=" +
				category_name.replace("&", "$") + "&field=" + field;
		
		System.out.println(get_response(url_name));
	}
	
	/**
	 * 获取给定ASIN的商品信息
	 * */
	public static void get_asin_commodity(){
		
		String asin = "B002GCOV1O";
		
		String field = "[\"ASIN\",\"productInfo\"]";
		
		String url_name = BASE_URL + asin +
				"?field=" + field;
		
		System.out.println(get_response(url_name));
	}
	
	public static void main(String[] args){
		get_all_caetgory();
		get_specified_commodity();
		get_asin_commodity();
	}
}
