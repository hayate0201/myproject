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
        #存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        #存放程序是否继续运行的变量
        self.enable = False
    #传入某一页的索引获得页面代码
    def getPage(self,pageIndex):
        try:
            url='http://www.qiushibaike.com/hot/page/' + str(self.pageIndex);
            #构建请求的request
            request=urllib2.Request(url,headers=self.headers)
            #利用urlopen获取页面代码
            response=urllib2.urlopen(request)
            #将页面转换成UTF-8编码
            pageCode=response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print "连接错误，错误原因：",e.reason
                return None
    #传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        print pageCode

        if not pageCode:
            print "页面加载失败...."
            return None
        #进行正则切割
        pattern=''
        '''pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?'+
                         'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
        '''
        items = re.findall(pattern,pageCode)
        print 123
        print items
        exit(1)
        #用来存储每页的段子们
        pageStories = []
        #遍历正则表达式匹配的信息
        for item in items:
            #是否含图片
            haveImg = re.search("img",item[3])
            #如果不含图片，把它加入到list中
            if not haveImg :
                replaceBR = re.compile('<br/>')
                text=re.sub(replaceBR,"\n",item[1])
                #item[0]是一个段子的发布者，item[1]是内容，item[2]是发布时间,item[4]是点赞数
                pageStories.append([item[0].strip(),text.strip(),item[2].strip(),item[4].strip()])
        return pageStories

    #加载并提取页面的内容，加入到列表
    def loadPage(self):
        #如果当前未看得页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                #获取新一页
                pageStories=self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    #获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1
        #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历一页的段子
        for story in pageStories:
            #等待用户输入
            input = raw_input()
            #每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            #如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t发布时间:%s\t赞:%s\n%s" %(page,story[0],story[2],story[3],story[1])

    #开始方法
    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        #使变量为True，程序可以正常运行
        self.enable = True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                #从全局list中获取一页的段子
                pageStories = self.stories[0]
                #当前读到的页数加一
                nowPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
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