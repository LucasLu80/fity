#!/usr/bin/python
# -*- coding: utf-8 -*-
# From http://71.6.135.131.ipaddress.com/ Get info
#encoding=utf-8

import urllib2
import httplib
import cookielib
import re
import time
import random
import socket




def UseProxy(proxy):
  
  #proxy = 'http://202.106.16.36:3128'
  try:
    proxy_handler=urllib2.ProxyHandler({'http':proxy})
    opener = urllib2.build_opener(proxy_handler,urllib2.HTTPHandler)
    urllib2.install_opener(opener)  
    return urllib2
  except httplib.BadStatusLine as e:
    print 'httplib.BadStatusLine...'
    return None
  
  

def readhtml(url):
  
  #proxy = 'http://user:123456@proxy.test.com:8080'
  #proxy_handler=urllib2.ProxyHandler({'http':proxy})
  #-----
  #opener = urllib2.build_opener(proxy_handler,urllib2.HTTPHandler)
  
  #urllib2.install_opener(opener)
  #opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1')]

  Accept_Encoding = "gzip,deflate,sdch"
  Proxy_Connection= "keep-alive"
  refer_data =  url
  
  global html

  MaxAllowRetryNumber = 2
  for tries in range(MaxAllowRetryNumber+1):
    count = random.randint(0,9)
    count2 = random.randint(0,9)
    count3 = random.randint(0,9)
    heard_data = "Mozilla/4.%s (compatible; MSIE 6.%s; Windows NT 5.%s) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36" %(count,count2,count3)
    
    Cookie = "dtsession=14ilqnb9tjv7riaf4ad1ucpa75; _ga=GA1.2.232827335.1452131789; \
            csrftoken=967995b98624b3bcec5f2132e38fa8af; __utma=247745176.232827335.1452131789.1452232953.1452475670.2;\
            __utmb=247745176.165.9.1452476724895; __utmc=247745176;\
            __utmz=247745176.1452232953.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
    
    headers={"User-Agent":heard_data,"Referer":refer_data,"Accept-Encoding":Accept_Encoding,"Proxy-Connection":Proxy_Connection,"Cookie":Cookie}
  
    socket.setdefaulttimeout(20) 
         
    try:
      #print tries
      req=urllib2.Request(url,headers=headers)  
      response=urllib2.urlopen(req) #timeout = 30 
      html = response.read()
      response.close()#后加入的
      break
    except urllib2.HTTPError as e:
      #print 'urllib2.HTTPError...tries=%d' %tries
      time.sleep(10*(tries+1))
      continue
    
    except httplib.BadStatusLine as e:
      #print 'httplib.BadStatusLine...tries=%d' %tries
      time.sleep(10*(tries+1))
      continue
      
    except socket.timeout as e:
      #response.close()#后加入的
      #print 'socket.timeout Error tries=%d' %tries
      time.sleep(30*(tries+1))
      continue
      
    except socket.error as e:
      #response.close()#后加入的
      #print 'socket.error Error tries=%d' %tries
      time.sleep(30*(tries+1))
      continue
  
    if tries > MaxAllowRetryNumber : html = None
    
    return html


def getKeynubmer(page,key):
  
  global wordList
  wordList = re.findall(re.compile(key), page) #寻找有几个<br>
  if wordList is None: return None
    
  return wordList


    


def getDataAtoB(page,A,B):
  '''
  在page中查找 A 到 B 之间的数据 
  '''
  start_link = page.find(A)
  if start_link == -1:
    print 'no found A to B'
    return None
  start_quote = page.find('//', start_link+1) #可以去掉
  end_quote = page.find(B, start_quote + 2)
  findword=page[start_quote+2:end_quote-1] 
  
  return findword,end_quote



def readfile2line(filename):
  '''
  读取filename文件内容，返回里面的一行一行的数据 （ip地址）
  '''
  f=open(filename,'r')
  Allfileline = f.readlines()
  f.close()

  return Allfileline 


def writeline(newline):
  '''
  读取当前目录下的mylog.txt文件并写入新的一行newline
  '''
  import os
  filename = 'mylog_w_4.txt'
  if os.path.exists(filename):
    f=open(filename,'a+')
  else:
    f=open(filename,'w')

  f.write(newline)
  f.write('\n')
  f.close()




def mymain(ip):
    '''
    这个是本程序的主函数
    '''
    global proxynum
  
  
    #ip = '188.138.1.218'
    urlfile = 'http://www.sitedossier.com/ip/%s' % ip #以文件的形式打开一个网页  http://www.sitedossier.com/ip/114.111.135.111
  
    #print '---------------------------------------------------------------'
    #print urlfile
  
    page = readhtml(urlfile)

    #print page
    
    if page is None:
      print 'readhtml is None'
      return False
    
    # Word contains letters A-Z only; case does not matter.
    #出现注册码
    TestShow = 'Word contains letters A-Z only; case does not matter.'
    TestShownubmer = getKeynubmer(page, TestShow)
    #print 'TestShownubmer = %d ' %TestShownubmer    
    if TestShownubmer==1:
      print 'The Web Display registration code!ip=%s' %ip
      #ipproxylist = ['202.106.16.36:3128','120.132.132.119:8080','110.153.9.250:80','202.202.1.189:80','202.112.113.7:80' ]
      #proxy = 'http://%s' %
      #urllib2 = UseProxy(proxy)
      return False      
    
    
  
    mydata={}
    mydata[ip]={}
  
    origin = urlfile 
    mydata[ip][origin] = {}
    #mydata[ip]['origin'] = origin
  
    
    #计算有多少个结果
    Isok = '<li> &nbsp; <a href='
    keynub = getKeynubmer(page, Isok)
    #print 'Isok = %d ' %keynub
       
    
    #没有任何数据
    IsNoDataok = 'No data currently available'
    NoDatakeynub = getKeynubmer(page, IsNoDataok)
    #print 'IsNoDataok = %d ' %NoDatakeynub    
    if NoDatakeynub==1:
      print '%s have not Hostname!' %ip
      return False
  
  
    #Hostname = getPageKey(page,'<tr><th>Host of this IP')
    Hostname = []
    start_link = page.find('<li> &nbsp; <a href=')
    findpage = page[start_link+18:]
    
    for one in range(keynub):
      oneHostname,endlink = getDataAtoB(findpage,'http://','</a>')
      Hostname.append(oneHostname)
      findpage = findpage[endlink:]
      
    #可能还有存在翻页情况
    #<a href="/ip/65.55.53.233/101"><b>Show remaining
    
    #print 'Hostname: %s' %Hostname
    
    mydata[ip][origin]['Hostname'] = Hostname
    
    #print mydata
    #writeline(mydata)
    
    writeline(repr(mydata))
    return True
  

if __name__=='__main__':
  
  iplines = readfile2line('mylog-4.txt')
  count=0
  add = 0
  for ipone in iplines:
      data = ipone.strip('\n')
      wordList = re.search(re.compile('\d+\.\d+\.\d+\.\d+'), data)
      if wordList is not None:
        one_ip = wordList.group()      
        
        flag = mymain(one_ip)
        
        if flag is False:
          print '%s is not have hostname!' %one_ip
          add = add + 1    #当出现错误时候，说明可能 对方进行限制，因此要减速
          time.sleep(add*2)
        else :
          count = count+1
          print '%s is ok!' %one_ip
          count = random.randint(0,15)
          count = count*2 + add
          time.sleep(count)
        
  print 'All line ok!!!'
  
  
  #http://114.111.135.111.ipaddress.com
  
  #mymain('65.55.53.233')#65.55.53.233


