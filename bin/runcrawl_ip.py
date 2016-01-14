#! /usr/bin/env python
# -*- coding: utf-8 -*-、



from subprocess import call
import os
import shutil
import argparse

#from request import scanfile

#命令形式： py       -命令参数f   被测ip文件
#          this.py   -f          ipfile.txt


def crwalip(web,ip):
    
    return




crawlipweb = ['whatismyipaddress.com',]

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i',dest='ip',
                            help="Show one IP's hostname, IP is likes 192.168.1.2")

    parser.add_argument('-f',dest='ipfile',
                           help='Crawl hostname From file, IPFILE is a txt file include all ip address')  
    
    parser.add_argument('--output',
                        choices=['List', 'JSON', 'XML'],
                        default='List',
                        help='select output method for results')  
    
    parser.add_argument('--processes', metavar='COUNT', type=int, default=0,
                        help='run COUNT nmap processes in parallel '
                        '(When the data is more)')    

    args = parser.parse_args()

   
    scanfile=['114.111.135.111','188.138.1.218']

    if args.ipfile is not None:
        for line in scanfile:
            #commandline = "python request/%s -l %s" %(line,args.ipfile)
            print line
        
    elif args.ip is not None:
        for web in crawlipweb:
            print crwalip(web,args.ip)
    else:
        print "'-h' to help"