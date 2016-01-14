#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file is part of FiTy.
# Copyright 2016 - 
#

'''
这是Fity程序一部分，主要是定义函数，关于ip 到 域名

'''

#第一次编写,时间2016-1-14,版本A_2016-1-14-0825




import urllib2
import httplib
import cookielib
import re
import time
import random
import socket




def UseProxy(ip):
    '''
    用来设置代理服务器地址
    '''

    proxy = 'http://%s' %ip
    try:
        proxy_handler=urllib2.ProxyHandler({'http':proxy})
        opener = urllib2.build_opener(proxy_handler,urllib2.HTTPHandler)
        urllib2.install_opener(opener)  
        return urllib2
    except httplib.BadStatusLine as e:
        print 'httplib.BadStatusLine...'
        return None
    
    
def CookieSet(cookie):
    '''
    用来产生随机cookie，使服务器端无法判断是否为一台机器
    '''

            
    return cookie


def TestProxyWebIs(proxy):
    '''
    测试代理服务器是否有用。用百度网址进行测试
    '''
    
    url = 'http://www.baidu.com'

    urllib2 = UseProxy(proxy)
    if urllib2 is None: return False
  
    heard_data = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"
    Accept_Encoding = "gzip,deflate,sdch"
    Proxy_Connection= "keep-alive"
    #refer_data =  proxy 

    headers={"User-Agent":heard_data,"Accept-Encoding":Accept_Encoding,"Proxy-Connection":Proxy_Connection,}

    for i in range(3):
        try:
            req=urllib2.Request(url,headers=headers)  
            response=urllib2.urlopen(req,timeout=20) #timeout = 30 
            html = response.read()
            response.close()#后加入的   
        except urllib2.URLError as e:
            time.sleep(i*10 + 1)
            continue
        except socket.timeout as e:
            time.sleep(i*10 + 1)
            continue
        except socket.error as e:
            time.sleep(i*10 + 1)
            continue
        else:
            #print html
            wordList = re.findall(re.compile('<title>百度一下，你就知道</title>'), html)
            if wordList is not None: return True
            return False      

    return False
  
  

def readhtml(url,proxy=None):
    '''
    读取网页内容
    '''

    Accept_Encoding = "gzip,deflate,sdch"
    Proxy_Connection= "keep-alive"
    refer_data =  url
    
    global urllib2
    
    if proxy is not None:urllib2 = UseProxy(proxy)

    global html

    MaxAllowRetryNumber = 2
    for tries in range(MaxAllowRetryNumber+1):
        count = random.randint(0,9)
        count2 = random.randint(0,9)
        count3 = random.randint(0,9)
        heard_data = "Mozilla/4.%s (compatible; MSIE 6.%s; Windows NT 5.%s) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36" %(count,count2,count3)

        Cookie = "pt=0c88e81172efbe163cd87a86755ac4c6; \
           __gads=ID=faf638a1bdc1ad28:T=1451895315:S=ALNI_MZX591my2HYtEwIAjjXPfVKA49GYA; \
           __qca=P0-1785519242-1451895190466;\
           __utmt_gwo=1; _gat=1; _ga=GA1.2.2004064199.1451895184;\
           __utma=53830638.2004064199.1451895184.1452222464.1452227341.8;\
           __utmb=53830638.2.10.1452227341; \
           __utmc=53830638; \
           __utmz=53830638.1451895268.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"

        headers={"User-Agent":heard_data,"Referer":refer_data,"Accept-Encoding":Accept_Encoding,"Proxy-Connection":Proxy_Connection,"Cookie":Cookie}

        socket.setdefaulttimeout(20) 
        
        CookieSet(Cookie)

        try:
            #print tries
            req=urllib2.Request(url,headers=headers)  
            response=urllib2.urlopen(req) #timeout = 30 
            html = response.read()
            response.close()#后加入的
        except urllib2.HTTPError as e:
            print 'urllib2.HTTPError...tries=%d' %tries
            time.sleep(10*(tries+1))
            continue

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
        else:
            return html
        
    return None



def getDataAtoB(page,A_key,B_key,**theRest):
    '''
    在网页page中，查找 A_key_2 B_key之间的数据 
    ,其中A_key是起使关键字，最好是一次定位，A_key_2是在A_key后面的关键字，用于关键定位
         B_key是最后的关键字
         A_nub 和 B_nub 可对关键字 A_key_2 与 B_key 位置的移动 
         
     例如 <th>Decimal:</th><td>1919911791</td>    
        A_key = Decimal ，A_key_2 = </t ,A_nub = 9
        B_key = </t  B_nub = 0
        
     返回结果： 1919911791，endlink
        
    '''
    A_key_2 = A_key[1:]
    A_nub = 0
    B_nub = 0
    for x in theRest:
        if x == 'A_key_2' : A_key_2 = theRest[x]
        if x == 'A_nub' : A_nub = theRest[x]
        if x == 'B_nub' : B_nub = theRest[x]

    #print A_key_2,A_nub,B_nub
    start_link = page.find(A_key)
    if start_link == -1:
        print 'no found'
        return None,None
    start_quote = page.find(A_key_2, start_link+1) #可以去掉
    end_quote = page.find(B_key, start_quote + 1)
    findword=page[start_quote + A_nub:end_quote+B_nub] 

    #print 'getdata = %s' % findword
    return findword,end_quote



def readfile2line(filename):
    '''
    读取filename文件内容，返回里面的一行一行的数据
    '''
    f=open(filename,'r')
    Allfileline = f.readlines()
    f.close()

    return Allfileline 

def writeline2file(newline,newfile):
    '''
    把newline 写入newline文件中
    '''
    import os
    if os.path.exists(newfile):
        f=open(newfile,'a+')
    else:
        f=open(newfile,'w')

    f.write(newline)
    f.write('\n')
    f.close()