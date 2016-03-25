__author__ = 'apple'
#coding=gbk
import urllib
import urllib2
import re
import thread
import time
class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.headers={
            'Accept':	'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':	'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Cache-Control':	'max-age=0',
            'Connection':	'keep-alive',
            'Host':	'www.qiushibaike.com',
            'If-None-Match':	'W/"f1c80cef478744b35e7876abd5a0efd52e3b375c"',
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0'
            #'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        }
        #��Ŷ��ӵı�����ÿһ��Ԫ����ÿһҳ�Ķ�����
        self.stories = []
        #��ų����Ƿ�������еı���
        self.enable = False
    #����ĳһҳ���������ҳ�����
    def getPage(self,pageIndex):
        try:
            url='http://www.qiushibaike.com/hot/page/' + str(self.pageIndex);
            #���������request
            request=urllib2.Request(url,headers=self.headers)
            #����urlopen��ȡҳ�����
            response=urllib2.urlopen(request)
            #��ҳ��ת����UTF-8����
            pageCode=response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print "���Ӵ��󣬴���ԭ��",e.reason
                return None
    #����ĳһҳ���룬���ر�ҳ����ͼƬ�Ķ����б�
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        print pageCode

        if not pageCode:
            print "ҳ�����ʧ��...."
            return None
        #���������и�
        pattern=''
        '''pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?'+
                         'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
        '''
        items = re.findall(pattern,pageCode)
        print 123
        print items
        exit(1)
        #�����洢ÿҳ�Ķ�����
        pageStories = []
        #����������ʽƥ�����Ϣ
        for item in items:
            #�Ƿ�ͼƬ
            haveImg = re.search("img",item[3])
            #�������ͼƬ���������뵽list��
            if not haveImg :
                replaceBR = re.compile('<br/>')
                text=re.sub(replaceBR,"\n",item[1])
                #item[0]��һ�����ӵķ����ߣ�item[1]�����ݣ�item[2]�Ƿ���ʱ��,item[4]�ǵ�����
                pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[4].strip()])
        return pageStories

    #���ز���ȡҳ������ݣ����뵽�б�
    def loadPage(self):
        #�����ǰδ����ҳ������2ҳ���������һҳ
        if self.enable == True:
            if len(self.stories) < 2:
                #��ȡ��һҳ
                pageStories=self.getPageItems(self.pageIndex)
                #����ҳ�Ķ��Ӵ�ŵ�ȫ��list��
                if pageStories:
                    self.stories.append(pageStories)
                    #��ȡ��֮��ҳ��������һ����ʾ�´ζ�ȡ��һҳ
                    self.pageIndex += 1
        #���ø÷�����ÿ���ûس���ӡ���һ������
    def getOneStory(self,pageStories,page):
        #����һҳ�Ķ���
        for story in pageStories:
            #�ȴ��û�����
            input = raw_input()
            #ÿ������س�һ�Σ��ж�һ���Ƿ�Ҫ������ҳ��
            self.loadPage()
            #�������Q��������
            if input == "Q":
                self.enable = False
                return
            print u"��%dҳ\t������:%s\t����ʱ��:%s\t��:%s\n%s" %(page,story[0],story[2],story[3],story[1])

    #��ʼ����
    def start(self):
        print u"���ڶ�ȡ���°ٿ�,���س��鿴�¶��ӣ�Q�˳�"
        #ʹ����ΪTrue�����������������
        self.enable = True
        #�ȼ���һҳ����
        self.loadPage()
        #�ֲ����������Ƶ�ǰ�����˵ڼ�ҳ
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                #��ȫ��list�л�ȡһҳ�Ķ���
                pageStories = self.stories[0]
                #��ǰ������ҳ����һ
                nowPage += 1
                #��ȫ��list�е�һ��Ԫ��ɾ������Ϊ�Ѿ�ȡ��
                del self.stories[0]
                #�����ҳ�Ķ���
                self.getOneStory(pageStories,nowPage)
spider = QSBK()
spider.start()
'''
try:
    request = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(request)
    print response.read()
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
'''
'''
headers = {
'Accept':	'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':	'gzip, deflate',
'Accept-Language':	'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Cache-Control':	'max-age=0',
'Connection':	'keep-alive',
'Host':	'www.qiushibaike.com',
'If-None-Match':	'W/"f1c80cef478744b35e7876abd5a0efd52e3b375c"',
'User-Agent':	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:38.0) Gecko/20100101 Firefox/38.0'}
data=''
request=urllib2.Request("http://www.qiushibaike.com/",headers=headers)
response = urllib2.urlopen(request)
print response.read()
'''