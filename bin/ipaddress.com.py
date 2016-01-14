#!/usr/bin/python
# -*- coding: utf-8 -*-
# From http://71.6.135.131.ipaddress.com/ Get info
#encoding=utf-8

import urllib2
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

  MaxAllowRetryNumber = 3
  for tries in range(MaxAllowRetryNumber+1):
    count = random.randint(0,9)
    count2 = random.randint(0,9)
    count3 = random.randint(0,9)
    heard_data = "Mozilla/4.%s (compatible; MSIE 6.%s; Windows NT 5.%s) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36" %(count,count2,count3)
    
    count4 = random.randint(1,19) % 2
    if count4 ==1 : cookie_data = "utmz=258263583.1353373445.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
    else: cookie_data = "utmz=10930924.1452233205.1.1.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=65.55.53.233"
  
    Cookie = "    __utmt=1; \
      __utma=10930924.924608010.1452233205.1452233205.1452241540.2;\
      __utmb=10930924.1.10.1452241540; __utmc=10930924; \
      __%s" % cookie_data   

    headers={"User-Agent":heard_data,"Referer":refer_data,"Accept-Encoding":Accept_Encoding,"Proxy-Connection":Proxy_Connection,"Cookie":Cookie}
  
    socket.setdefaulttimeout(20) 
         
    try:
      #print tries
      req=urllib2.Request(url,headers=headers)  
      response=urllib2.urlopen(req) #timeout = 30 
      html = response.read()
      response.close()#后加入的
      break
    except socket.timeout as e:
      response.close()#后加入的
      print 'socket.timeout Error tries=%d' %tries
      time.sleep(30*(tries+1))
      continue
      
    except socket.error as e:
      response.close()#后加入的
      print 'socket.error Error tries=%d' %tries
      time.sleep(30*(tries+1))
      continue
  
  if tries > 3 : return None
  
  return html


    
def getPageKey(page,key):
  '''
  在page中查找 从 key:</th>...到... </t 之间的数据 
  eg:        IP:</th><td>66.240.192.138</td>    =>  66.240.192.138
       Hostname:</th><td>census8.shodan.io</td> =>  census8.shodan.io
  '''
  
  findkey='%s:</th>' %key
  start_link = page.find(findkey)
  if start_link == -1:
    #print 'GetPageKey:[%s not in Page]' %key
    return None
  start_quote = page.find('/', start_link+1)
  end_quote = page.find('/t', start_quote + 1)
    
  findword=page[start_quote+8:end_quote-1] # end_quote=/t; end_quote-1=<;
  
  return findword





def getDataAtoB(page,A,B):
  '''
  在page中查找 A='UserComments..>' ...  B='Enter up to 500 characters' 之间的数据 
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
  filename = 'mylog_w_2.txt'
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
    urlfile = 'http://%s.ipaddress.com' % ip #以文件的形式打开一个网页   http://71.6.135.131.ipaddress.com
  
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
  
    #ip = getPageKey(page,'IP Address')
    #print 'IP Address: %s' %ip
    #
  
    Hostname = getPageKey(page,'<tr><th>Host of this IP')
    #print 'Hostname: %s' %Hostname
    if Hostname is not None :mydata[ip][origin]['Hostname'] = Hostname
    else:
      print '%s have not Hostname!' %ip
      return False
    
    Organization = getPageKey(page,'Organization')
    #print 'Organization: %s' %Organization
    mydata[ip][origin]['Organization'] = Organization   
    
    ISP = getPageKey(page,'ISP')
    #print 'ISP: %s' %ISP
    mydata[ip][origin]['ISP'] = ISP   
    
    # Updated
  
  
    #print '---------------------------------------------------------------'
  
    City = getPageKey(page,'City')
    #print 'City: %s' %City
    mydata[ip][origin]['City'] = City
  
    #Country

    State = getPageKey(page,'State')
    #print 'State: %s' %State
    mydata[ip][origin]['State'] = State
    
    
    
    #        State:</th><td>California</td></tr>
    #<tr><th>Postal Code:</th><td>92123</td></tr>
    #<tr><th>Timezone:</th><td>America/Los_Angeles</td></tr>
    #<tr><th>Local Time:</th><td>01/08/2016 11:17 PM</td></tr>    
  
   
  
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
  
  #mymain('114.111.135.111')


