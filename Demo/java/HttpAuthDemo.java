package com.skymoney.basic_demo;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import sun.misc.*;

public class HttpAuthDemo {
	public HttpAuthDemo(){}
	
	private static String encode_base64(String input){
		return new BASE64Encoder().encode(input.getBytes());
	}
	
	public static void fetch_data() throws IOException{
		String username = "";
		String passwd = "";
		String token = "";
		BufferedReader reader = null;
		String result = "";
		
		URL url = new URL("http://112.124.1.3:8020");
		
		URLConnection connection = url.openConnection();
		
		//设置请求头内容，主要是认证信息
		String baseString = encode_base64(username + ":" + passwd).replace("\n", "");
		connection.setRequestProperty("Authorization", 
				"Basic " + baseString);
		
		connection.connect();
		
		//获取响应信息
		reader = new BufferedReader(new InputStreamReader(
				connection.getInputStream()));
		
		String line;
		//获取返回内容
		while((line = reader.readLine()) != null){
			result += line;
		}
		
		System.out.println(result);
	}
	
	public static void main(String[] args) throws IOException{
		fetch_data();
	}
}
