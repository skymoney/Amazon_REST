package com.moneyc.util;

import java.io.UnsupportedEncodingException;

/**
 * Base64编码和解码 Java实现
 * 可以针对中文英文等字符串的编码
 * 解码部分对于中文是解码到utf-8编码
 * */
public class Base64 {
	//映射表
	final String mappingStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	
	public Base64(){}
	
	/**
	 * 编码部分
	 * */
	public String encode(String srcStr) throws UnsupportedEncodingException{
		byte[] str_list = srcStr.getBytes("UTF-8");
		
		String currentFixStr = "";
		String outputStr = "";
		for(int i=0;i<str_list.length; i++){
			String current = Integer.toBinaryString(0xFF & (int)str_list[i]);
			
			//为了补全到标准的8比特位
			if(current.length() < 8){
				int originLength = 8 - current.length();
				for(int j=0;j < originLength;j++){
					current = "0" + current;
				}
			}
			String currentEncode = currentFixStr + current.substring(0, 
					6-currentFixStr.length());
			currentFixStr = current.substring(6-currentFixStr.length());
			
			outputStr += mappingStr.charAt(Integer.parseInt(currentEncode, 2));
			
			if(currentFixStr.length() == 6){
				outputStr += mappingStr.charAt(Integer.parseInt(currentFixStr, 2));
				currentFixStr = "";
			}
		}
		//字节数刚好
		if(currentFixStr.length() == 6){
			outputStr += mappingStr.charAt(Integer.parseInt(currentFixStr, 2));
		}
		
		//只有一个字节多出来的情况，多出2个比特位
		if(currentFixStr.length() == 2){
			outputStr += mappingStr.charAt(Integer.parseInt(currentFixStr + "0000", 2));
			outputStr += "==";
		}
		
		//多出两个字节，这样多出4个比特位
		if(currentFixStr.length() == 4){
			outputStr += mappingStr.charAt(Integer.parseInt(currentFixStr + "00", 2));
			outputStr += "=";
		}
		
		return outputStr;
	}
	
	public String decode(String encriptStr){
		String outputStr = "";
		int removeCount = 0;
		String originStr = "";
		if(encriptStr.endsWith("==")){
			//补全两个=，对应多出一个字节的情况，那么最后转码时去除最后四位
			removeCount = 4;
		}else{
			if(encriptStr.endsWith("=")){
				removeCount = 2;
			}else{
				removeCount = 0;
			}
		}
		String toDealStr = encriptStr.replaceAll("=", "");  //去除所有补全的 =
		
		//转化成二进制，补位得到原字符串
		for(int i=0;i<toDealStr.length();i++){
			String bin = Integer.toBinaryString(0xFF & mappingStr.indexOf(toDealStr.charAt(i)));
			
			if(bin.length() < 8){
				int toComplete = 8 - bin.length();
				for(int j=0; j<toComplete; j++){
					bin = "0" + bin;
				}
			}
			originStr += bin.substring(2);
		}
		
		originStr = originStr.substring(0, originStr.length() - removeCount);
		
		int idx = 0;
		//每8个比特位一组，得到原字符
		while(idx < originStr.length() ){
			String bin = originStr.substring(idx, idx+8);
			
			if(bin.startsWith("1")){
				//非ascii字符
				String firstChar = Integer.toHexString(Integer.parseInt(bin.substring(0, 4), 2));
				String secondStr = Integer.toHexString(Integer.parseInt(bin.substring(4, 8), 2));
				outputStr += "\\x" + firstChar + secondStr;
			}else{
				//正常的ascii字符
				outputStr += (char)Integer.parseInt(bin, 2);
			}
			idx += 8;			
		}
		
		return outputStr;
	}
	
	public static void main(String[] args) throws UnsupportedEncodingException{
		String test = "程yest";
		System.out.println(new Base64().encode(test));
		
		String input = "56iLeWVzdA==";
		System.out.println(new Base64().decode(input));
	}
}

