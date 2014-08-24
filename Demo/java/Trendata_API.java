package com.moneyc.demo;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.URL;
import java.net.URLConnection;

import com.moneyc.util.Base64;

public class Trendata_API {
	/**
	 * Base64转码
	 * */
	public String encodeBase64(String input) throws UnsupportedEncodingException{
		return new Base64().encode(input);
	}
	
	public void fetch_data() throws IOException{
		String username = "";
		String passwd = "";
		String token = "";
		String target_url = "http://112.124.1.3:8020/commodity/B000GHVGRI?field=[\"productInfo\", \"ASIN\"]";
		
		BufferedReader reader = null;
		String line = null;
		String result = "";
		
		URL url = new URL(target_url);
		URLConnection connection = url.openConnection();
		
		//设置请求头内容，主要是认证消息
		connection.setRequestProperty("Authorization", 
				"Basic " + encodeBase64(username + ":" + passwd));
		//或者使用token
		//connection.setRequestProperty("Authorization", 
		//		"Basic " + encodeBase64(token + ": "));
		
		connection.connect();
		
		reader = new BufferedReader(new InputStreamReader(
				connection.getInputStream()));
		
		while((line = reader.readLine()) != null){
			result += line;
		}
		
		System.out.println(result);
		
		//下面可以使用Json-lib 或者 org.json处理数据
	}
	
	public static void main(String[] args) throws IOException{
		new Trendata_API().fetch_data();
	}
}
