#!/usr/bin/python
# -*- coding: utf-8 -*-
# From http://71.6.135.131.ipaddress.com/ Get info
#encoding=utf-8

import urllib2
import cookielib
import re
import time
import random



def readhtml(url):
 
  count = random.randint(0,9)
  count2 = random.randint(0,9)
  count3 = random.randint(0,9)
  
  heard_data = "Mozilla/4.%s (compatible; MSIE 6.%s; Windows NT 5.%s) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36" %(count,count2,count3)
  refer_data =  url 
  Accept_Encoding = "gzip,deflate,sdch"
  Proxy_Connection= "keep-alive"
  Cookie = "pt=0c88e81172efbe163cd87a86755ac4c6; \
           __gads=ID=faf638a1bdc1ad28:T=1451895315:S=ALNI_MZX591my2HYtEwIAjjXPfVKA49GYA; \
           __qca=P0-1785519242-1451895190466;\
           __utmt_gwo=1; _gat=1; _ga=GA1.2.2004064199.1451895184;\
           __utma=53830638.2004064199.1451895184.1452222464.1452227341.8;\
           __utmb=53830638.2.10.1452227341; \
           __utmc=53830638; \
           __utmz=53830638.1451895268.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
  
  headers={"User-Agent":heard_data,"Referer":refer_data,"Accept-Encoding":Accept_Encoding,"Proxy-Connection":Proxy_Connection,"Cookie":Cookie}
  
  req=urllib2.Request(url,headers=headers)
  
  try:
    response=urllib2.urlopen(req,timeout = 30) 
  except urllib2.URLError,e:
    #print e.code
    print e.reason
    print '延长时间，请等待……'
    count = random.randint(60,600)
    count = count * 2
    response=urllib2.urlopen(req,timeout = 60) 
    
  html = response.read()
   
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
    print None
  start_quote = page.find('/', start_link)
  end_quote = page.find('/t', start_quote + 1)
    
  findword=page[start_quote+8:end_quote-1] # end_quote=/t; end_quote-1=<;
  
  return findword


def getPageKeytoEnd(page,key,end):
  '''
  在page中查找 从 key:</th>...到... end 之间的数据 
  '''
  
  findkey='%s:</th>' %key
  start_link = page.find(findkey)
  if start_link == -1:
    print None
  start_quote = page.find('/', start_link)
  end_quote = page.find(end, start_quote + 1)
    
  findword=page[start_quote+8:end_quote] 
  
  return findword


def getDataAtoB(page,A,B):
  '''
  在page中查找 A='UserComments..>' ...  B='Enter up to 500 characters' 之间的数据 
  '''
  start_link = page.find(A)
  if start_link == -1:
    print 'no found'
    print None
  start_quote = page.find('>', start_link+1) #可以去掉
  end_quote = page.find(B, start_quote + 1)
  findword=page[start_quote+1:end_quote] 
  
  return findword,end_quote


def getWordandDate(page):
  '''
  在page中返回 .....句子A.......  截止<em ....和  开始 >- ....句子B.... 两个数据 
  '''
  start_link = page.find('<')
  if start_link == -1:
    print None,None
  A = page[0:start_link]
  
  start_quote = page.find('>', start_link+1)
  B = page[start_quote+4:] # >k-k
  
  #print A
  #print B
  return A,B


def findthreatword(page): 
  newpage = page.lower()
  threatword=['hack','attack','probe','connect','scan','attempt']
  allword = None
  datatime=  None     
  for oneword in threatword: 
    if oneword in newpage:
      allword,datatime = getWordandDate(page)
      break
      
  return oneword,allword,datatime


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
  filename = 'mylog_w.txt'
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
    urlfile = 'http://whatismyipaddress.com/ip/%s' % ip #以文件的形式打开一个网页
  
    #print '---------------------------------------------------------------'
    #print urlfile
  
    page = readhtml(urlfile)
  
    if page is None:
      return None
  
    mydata={}
    mydata[ip]={}
  
    origin = urlfile 
    mydata[ip]['origin'] = origin
  
    #ip = getPageKey(page,'IP')
    #print 'IP: %s' %ip
  
    Decimal = getPageKey(page,'Decimal')
    #print 'Decimal: %s' %Decimal
    mydata[ip]['Decimal'] = Decimal
  
    Hostname = getPageKey(page,'Hostname')
    #print 'Hostname: %s' %Hostname  
    mydata[ip]['Hostname'] = Hostname
  
    ASN = getPageKey(page,'ASN')
    #print 'ASN: %s' %ASN
    mydata[ip]['ASN'] = ASN
  
    ISP = getPageKey(page,'ISP')
    #print 'ISP: %s' %ISP
    mydata[ip]['ISP'] = ISP
  
    Organization = getPageKey(page,'Organization')
    #print 'Organization: %s' %Organization
    mydata[ip]['Organization'] = Organization
  
    Services = getPageKey(page,'Services')
    #print 'Services: %s' %Services  
    mydata[ip]['Services'] = Services
  
    #目前先不要这个数据
    #findip = getPageKey(page,'Type')
    #print 'Type: %s' %findip 
  
    #目前先不要这个数据
    #findip = getPageKey(page,'Assignment')
    #print 'Assignment: %s' %findip  
  
    #目前先不要这个数据
    #findip = getPageKey(page,'Blacklist')
    #print 'Blacklist: %s' %findip  
  
    #print '---------------------------------------------------------------'
  
    Continent = getPageKey(page,'Continent')
    #print 'Continent: %s' %Continent 
    mydata[ip]['Continent'] = Continent
  
    Country = getPageKeytoEnd(page,'Country',' <img')# 这里有一个空格
    #print 'Country: %s' %Country 
    mydata[ip]['Country'] = Country
  
    Latitude = getPageKeytoEnd(page,'Latitude','&nbsp')
    findone=getPageKeytoEnd(page,'Latitude','</td>')
    Latitude = Latitude[1:] + findone[-2] #注意在Latitude中，获取的第一个是\n，所以要去掉
    #print 'Latitude: %s' %Latitude
    mydata[ip]['Latitude'] = Latitude
  
    Longitude = getPageKeytoEnd(page,'Longitude','&nbsp')  
    findone=getPageKeytoEnd(page,'Longitude','</td>')
    Longitude = Longitude[1:] + findone[-2]
    #print 'Longitude: %s' %Longitude
    mydata[ip]['Longitude'] = Longitude
  
    #print '-----User Comments--------------------------------------------'
  
    findip,end_data = getDataAtoB(page,'User Comments','500 characters')
    #print findip
    wordList = re.findall(re.compile('<br>'), findip) #寻找有几个<br>
    #print "test word %d \n\n" %len(wordList)
  
    keyword={'hack':[],'attack':[],'probe':[],'connect':[],'scan':[],'attempt':[]} 
    count=0
    for i in range(len(wordList)):
      #print i
      if i==0 :
        findline,end_data = getDataAtoB(findip,'p','</em>')
        oneword,allword,datatime = findthreatword(findline)
        if allword is not None:keyword[oneword].append(allword+datatime)
  
      else:
        findline,end_data = getDataAtoB(findip[count:-1],'br','</em>')
        oneword,allword,datatime = findthreatword(findline)
        if allword is not None:keyword[oneword].append(allword+datatime)
  
      count = count + end_data
      #print keyword
      #print '--------------------------------------'      
  
    #print keyword
    mydata[ip]['keyword'] = keyword
  
    #print mydata
    #writeline(mydata)
    writeline(repr(mydata))
  

if __name__=='__main__':

  
  iplines = readfile2line('mylog_again.txt')
  count=0
  for ipone in iplines:
      data = ipone.strip('\n')
      wordList = re.search(re.compile('\d+\.\d+\.\d+\.\d+'), data)
      if wordList is not None:
        one_ip = wordList.group()      
        #print "%s is OK!" %one_ip
        mymain(one_ip)
        #count = count+1
        print '%s is ok!' %one_ip
        count = random.randint(0,15)
        count = count*2 + 1 
        time.sleep(count)
        
  print 'All line ok!!!'
  

#  count = random.randint(0,9)
#  count2 = random.randint(0,9)
#  count3 = random.randint(0,9)
#  heard_data = "Mozilla/4.%s (compatible; MSIE 6.%s; Windows NT 5.%s" %count

#  print heard_data
#  txtfile=open('mytxt.txt','w')
   
#  for s in wordList:
#    txtfile.write(s)
#    txtfile.write('\n')
    
#  txtfile.close()


