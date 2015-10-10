# coding:UTF-8
import urllib2,urllib
import re
import sys
import base64
import simplejson as json

class getdomain(object):
  def __init__(self):
		super (getdomain, self).__init__()
  def baidu(self,domain,page=10):
    list=[]
    for x in range(page):
	  i=x*10
	  url='http://www.baidu.com/s?wd=site:'+domain+'&pn='+str(i)+'&ie=utf-8'
	  request=urllib2.Request(url)
	  response=urllib2.urlopen(request).read()
	  p=re.compile(r'<span class="g">(.+?)/')
	  m=p.findall(response)
	  for x in m:
		list.append(x)
    return set(list)
	
  def bing(self,domain):
    list=[]
    key='HY5Eym8ueQukxTv9UfBT++54jhzoTo9kRLrH8Gn+jME'
    top=100
    skip=0
    format='json'
    action={}
    action['$top']=top
    action['$skip']=skip
    action['$format']=format
    action['Query']="'"+"site:"+domain+"'"
    url='https://api.datamarket.azure.com/Bing/Search/Web?'+urllib.urlencode(action)
    Auth='Basic '+base64.b64encode(':'+key)
    headers = {}  
    headers['Authorization']= Auth  
    request=urllib2.Request(url,headers=headers)
    response = urllib2.urlopen(request).read()
    result = json.loads(response)
    for x in range(top/2):
        list.append(result["d"]["results"][x]["DisplayUrl"])
    return set(list)
  
  def google(self,domain,page=10):
    list=[]
    start = page* 10 + 1
    cx='011056510141275609739:qijjdpnhap4'
    key='AIzaSyDxkaEwuollK2FN9OPlqhwtpy-s5QJyif0'
    for i in range(1,start,10):
		url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s&start=%d" % (key, cx, domain, i)	
		request=urllib2.Request(url)
		response = urllib2.urlopen(request).read()
		result = json.loads(response)
		for x in range(10):
			list.append(result["items"][x]["displayLink"])
    return set(list)

	
	
	
	
	
if __name__ == '__main__':
  keyword=sys.argv[1]
  result=[]
  list=[]
  getdomain=getdomain()
  result=getdomain.google(keyword)
  for i in result:
    list.append(i)
  result=getdomain.bing(keyword)
  for i in result:
    list.append(i)
  result=getdomain.baidu(keyword)
  for i in result:
    list.append(i)
  for i in set(list):
    print i
  f=open("result.txt","w")
  for i in set(list):
    f.write(i)
    f.write("\r\n")
  f.close
  