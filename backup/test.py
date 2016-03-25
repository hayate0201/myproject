__author__ = 'apple'
#-*- coding:utf-8 -*-
import urllib
import urllib2

class Spider:
    def __init__(self):
        self.siteUrl='https://service.cmbc.com.cn/pai_ms/cft/queryTssPrdInScreenfoForJson.gsp'
    def getPage(self,pageIndex):
        url=self.siteUrl+"?page="+str(pageIndex)+"&rows=10"
        print url
        request=urllib2.Request(url)
        response=urllib2.urlopen(request)
        return response

    def getContents(self,pageIndex):
        page=self.getPage(pageIndex)
spider =Spider()
spider.getContents(1)