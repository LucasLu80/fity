#!/usr/bin/python
# -*- coding: utf-8 -*-
#encoding=utf-8

# This file is part of FiTy.
# Copyright 2016 - 
#

'''
这是Fity程序一部分，主要是通过该域名网站 http://whatismyipaddress.com/，

从ip数据 爬取相应信息

'''


#第一次编写,时间2016-1-14,版本A_2016-1-14-0825


import sys

#import fity.utils

from fity.utils import *



def getPageKey(page,key):
    
    reword,endlink = getDataAtoB(page,key,'</t',A_nub=9,A_key_2='</t',B_nub=0)

    return reword

def getPageAtoB(page,A,B):
    
    reword,endlink = getDataAtoB(page,A,B,A_nub=9,A_key_2='/',B_nub=0)

    return reword    

def getPageAtoB2(page,A,B):
    
    reword,endlink = getDataAtoB(page,A,B,A_nub=1,A_key_2='>',B_nub=0)

    return reword,endlink


def getWordandDate(page):
    '''
    在page中返回 .....句子A.......  截止<em ....和  开始 >- ....句子B.... 两个数据 
    '''
    start_link = page.find('<')
    if start_link == -1:
        return None,None
    A = page[0:start_link]

    start_quote = page.find('>', start_link+1)
    B = page[start_quote+4:] # >k-k
    
    #print A,B
    return A,B


def findthreatword(page): 
    '''
    在page中查找 关键词(小写)
    '''
    newpage = page.lower()
    threatword=['hack','attack','probe','connect','scan','attempt']
    allword = None
    datatime=  None     
    for oneword in threatword: 
        if oneword in newpage:
            allword,datatime = getWordandDate(page)
            break

    return oneword,allword,datatime


def getwebinfo(page):
    webinfo={}
    
    listkey = ['Decimal','Hostname','ASN','ISP','Organization','Services','Continent']
    for one in listkey:
        webinfo[one] = getPageKey(page, one)
        
    webinfo['Country'] = getPageAtoB(page,'Country',' <img')# 这里有一个空格
    Latitude = getPageAtoB(page,'Latitude','&nbsp')
    findone=getPageAtoB(page,'Latitude','</td>')
    Latitude = Latitude[1:] + findone[-2] #注意在Latitude中，获取的第一个是\n，所以要去掉
    webinfo['Latitude'] = Latitude
    Longitude = getPageAtoB(page,'Longitude','&nbsp')  
    findone=getPageAtoB(page,'Longitude','</td>')
    Longitude = Longitude[1:] + findone[-2]
    webinfo['Longitude'] = Longitude  
    
    #------------------------------------------------
        
    findip,end_data = getPageAtoB2(page,'User Comments','500 characters')
    #print findip
    wordList = re.findall(re.compile('<br>'), findip) #寻找有几个<br>
    
    keyword={'hack':[],'attack':[],'probe':[],'connect':[],'scan':[],'attempt':[]} 
    
    count=0
    for i in range(len(wordList)):
        if i==0 :
            findline,end_data = getPageAtoB2(findip,'p','</em>')
            oneword,allword,datatime = findthreatword(findline)
            if allword is not None:keyword[oneword].append(allword+datatime)
    
        else:
            findline,end_data = getPageAtoB2(findip[count:-1],'br','</em>')
            oneword,allword,datatime = findthreatword(findline)
            if allword is not None:keyword[oneword].append(allword+datatime)
    
            count = count + end_data
            #print keyword
            #print '--------------------------------------'      
    
    #print keyword
    webinfo['keyword'] = keyword    
    
    return webinfo


def mymain(ip,proxy=None):
    
    url = 'http://whatismyipaddress.com/ip/%s' %ip  #114.111.135.111
    
    page = readhtml(url,proxy)
    if page is None:
        #print 'readhtml is None'
        return False    
    
    import gzip, StringIO
    page = gzip.GzipFile(fileobj=StringIO.StringIO(page), mode="r")
    page = page.read().decode('gbk').encode('utf-8')     
    
    listkey = getwebinfo(page)
    listkey['url'] = url
    
    return listkey
    
    
def whatismyipaddress(ip):
    '''
     从whatismyipaddress网址 查找ip
    '''
    data = {}
    data['ip']=ip
    data['source']=mymain(ip)
    
    return data


if __name__=='__main__':
    
    #iplist = ['202.106.16.36:3128','120.132.132.119:8080','110.153.9.250:80','202.202.1.189:80','202.112.113.7:80' ]
    #if TestProxyWebIs('202.202.1.189:80') is True :print 'okokok'
  
 
    print whatismyipaddress('114.111.135.111')
  
    