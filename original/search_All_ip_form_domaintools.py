#!/usr/bin/python
# -*- coding: utf-8 -*-
# From http://reverseip.domaintools.com/search/?q=65.55.53.233 Get info
#encoding=utf-8

#writed by 2016-1-11

import urllib2
import httplib
import cookielib
import re
import time
import random
import socket



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
  MaxAllowRetryNumber = 3
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
    except httplib.BadStatusLine as e:
      print 'httplib.BadStatusLine...tries=%d' %tries
      time.sleep(10*(tries+1))
      continue
      
    except socket.timeout as e:
      #response.close()#后加入的
      print 'socket.timeout Error tries=%d' %tries
      time.sleep(30*(tries+1))
      continue
      
    except socket.error as e:
      #response.close()#后加入的
      print 'socket.error Error tries=%d' %tries
      time.sleep(30*(tries+1))
      continue
  
  if tries > MaxAllowRetryNumber : html = None
  
  return html


def getKeynubmer(page,key):
  
  nubm=0
  wordList = re.findall(re.compile(key), page) #寻找有几个<br>
  if wordList is not None: nubm = len(wordList)
    
  return nubm


    


def getDataAtoB(page,A,B):
  '''
  在page中查找 A 到 B 之间的数据 
  '''
  start_link = page.find(A)
  if start_link == -1:
    print 'no found A to B'
    return None
  start_quote = page.find('>', start_link+1) #可以去掉
  end_quote = page.find(B, start_quote + 1)
  findword=page[start_quote+1:end_quote] 
  
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
  filename = 'mylog_w_3.txt'
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
  
    #ip = '188.138.1.218'
    urlfile = 'http://reverseip.domaintools.com/search/?q=%s' % ip #以文件的形式打开一个网页   http://71.6.135.131.ipaddress.com
  
    #print '---------------------------------------------------------------'
    #print urlfile
  
    page = readhtml(urlfile)
    
    import gzip, StringIO
    page = gzip.GzipFile(fileobj=StringIO.StringIO(page), mode="r")
    page = page.read().decode('gbk').encode('utf-8')
    
    #print page
  
    if page is None:
      print 'readhtml is None'
      return False
  
    mydata={}
    mydata[ip]={}
  
    origin = urlfile 
    mydata[ip][origin] = {}
    #mydata[ip]['origin'] = origin
  
    
    #<span title="%s"> %ip
    findkey = '<span title="%s">' %ip
    keynub = getKeynubmer(page, findkey)
    #print 'keynub = %d ' %keynub
    
    if keynub==0:
      print '%s have not Hostname!' %ip
      return False
  
  
    #Hostname = getPageKey(page,'<tr><th>Host of this IP')
    Hostname = []
    findpage = page
    for one in range(keynub):
      oneHostname,endlink = getDataAtoB(findpage,findkey,'</')
      Hostname.append(oneHostname)
      findpage = findpage[endlink:]
    
    #print 'Hostname: %s' %Hostname
    
    mydata[ip][origin]['Hostname'] = Hostname
    
    #print mydata
    #writeline(mydata)
    
    writeline(repr(mydata))
    return True
  

if __name__=='__main__':
  
  
  iplines = readfile2line('mylog_again.txt')
  count=0
  add = 0
  for ipone in iplines:
      data = ipone.strip('\n')
      wordList = re.search(re.compile('\d+\.\d+\.\d+\.\d+'), data)
      if wordList is not None:
        one_ip = wordList.group()      
        
        flag = mymain(one_ip)
        
        if flag is False:
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


