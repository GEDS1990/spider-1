#!/usr/bin/env python
#coding=utf-8
'''
    @Desc 主要用来抓取迅播影院（www.2tu.cc）电影下载链接还有电影名称的，蜘蛛：http://www.2tu.cc/GvodHtml/15.html
    @Author chenqing663@foxmail.com
    @Date 2013-07-06
'''

import re                       # 爬虫进么能够不用到正则表达式呢？
from bs4 import BeautifulSoup   # 需要安装的这个美丽的汤的：一个用着比较爽的html，xml解析模块
import urllib2                  # 当然，你也可以用其他你用着比较爽的模块，httplib,urllib,pycurl
from urlparse import urlparse   # 虽然这个模块不是必需的，但有了它，url解析起码简单很多

class xunbo(object):
    '''
    主要功能：取出最新电影下面的所有的下载链接，类似：
    ftp://dygod1:dygod1@d245.dygod.org:6017/[电影天堂www.dy2018.net].中国合伙人.HD.720p.国语中字.rmvb
    '''

    def __init__(self,num):
        self.num = num          #前多少页面的链接要爬，'http://www.2tu.cc/GvodHtml/15_'+ str(num) + '.html


    def list_url(self):
        '''
        主要功能：目录页url取出，比如：'http://www.2tu.cc/GvodHtml/15_'+ str(num) + '.html
        '''
        tmp_url = []
        host_prefix = 'http://www.2tu.cc/GvodHtml/'

        tmp_url = [host_prefix + '15.html']

        for i in range(2,self.num):
            tmp_url.append(host_prefix + '15_' + str(i) + '.html')

        return tmp_url

    def http_url(self):
        '''
        主要功能：取出电影的详细内容页，比如：
        http://www.2tu.cc/Html/GP15625.html
        '''
        url_to_work = []

        host = 'http://www.2tu.cc'

        for u in self.list_url():
            '''
            千万要注意这里的编码啊，不然你会受伤的......
            '''
            try:
                data = urllib2.urlopen(u).read().decode('gbk','ignore')

                data.encode('utf-8')
            except:
                pass
            try:
                soup = BeautifulSoup(data)

                link =  soup.findAll('h1',{"class":"c0071bc"})
                for a in link:
                    for url in  a.findAll('a'):
                       # print url.get_text(),host+url['href']   # url.get_text() 获取到的是电影名称
                        url_to_work.append(host+url['href'])
            except:
                pass

        return url_to_work


    def ftp_url(self,url):
        '''
        主要功能：从详细的页面取出下载电影的ftp链接
        '''
        ftp_link = ''
        try:
            data = urllib2.urlopen(url).read().decode('gbk','ignore').encode('utf-8')
            res = re.compile(r'(ftp://.*?\.rmvb)')
            try:
                ftp_link =  str(res.findall(str(data))[0]).split('###')[0].decode('utf-8')
                #print ftp_link
            except:
                pass

        except:
            pass

        return ftp_link

