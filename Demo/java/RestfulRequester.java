import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;


public class RestfulRequester {

	public static String requestRestful(String urlStr, Map urlParam) throws IOException{
	    String urlParamStr = "?";
	    String auth = "YjA1NTRkMzdhYjNjYWRmM2VlMDU0ZThmNTE4ZjNiMmI6";
	    if(!urlParam.isEmpty()){
	        //定义一个迭代器，并将MAP值的集合赋值
	        Iterator ups = urlParam.entrySet().iterator();
	        while(ups.hasNext()){
	            Map.Entry MUPS = (Map.Entry)ups.next();
	            urlParamStr += MUPS.getKey() + "=" + MUPS.getValue().toString().trim() + "&";
	        }
	        urlParamStr = urlParamStr.substring(0, urlParamStr.length() - 1);
	    }
	    //实例一个URL资源
	    URL url = new URL(urlStr + urlParamStr);
//	    System.out.println(url);
	    //实例一个HTTP CONNECT
	    HttpURLConnection connet = (HttpURLConnection) url.openConnection();
	    connet.setRequestMethod("GET");
	    connet.setRequestProperty("Authorization", "Basic "+ auth);
	    connet.setRequestProperty("Content-Type","application/x-www-form-urlencoded");
	    if(connet.getResponseCode() != 200){
	        throw new IOException(connet.getResponseMessage());
	    }
	    //将返回的值存入到String中
	    BufferedReader brd = new BufferedReader(new InputStreamReader(connet.getInputStream()));
	    StringBuilder  sb  = new StringBuilder();
	    String line;
	 
	    while((line = brd.readLine()) != null){
	        sb.append(line);
	    }
	    brd.close();
	    connet.disconnect();
	 
	    return sb.toString();
	}
	
	public static void main(String[] args){
		try {
			Map urlParam = new HashMap();
			urlParam.put("where", "ASIN==B00AC8SHDW");
			String result = RestfulRequester.requestRestful("http://112.124.1.3:5000/commodity", urlParam);
			System.out.println(result.length());
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
