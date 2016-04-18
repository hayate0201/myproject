#encoding=utf-8
#数据库测试
'''
import pymongo

conn = pymongo.MongoClient("127.0.0.1",27017)
db  = conn.test
content = db['bank_boc'].find()
print content
'''
import urllib2,urllib     # 把这两个库导入

url = 'https://api.douban.com/v2/book/user/ahbei/collections'  # 这是要请求的url

data={'status':'read','rating':3,'tag':'小说'}  # 根据api文档提供的参数，我们来获取一下阿北读过的书中，他标记了‘小说’这个标签的三星书籍，把这些参数值存在一个dict里

data = urllib.urlencode(data) # 把参数进行编码 

url2 = urllib2.Request(url,data) # 用.Request来发送POST请求，指明请求目标是之前定义过的url，请求内容放在data里

response = urllib2.urlopen(url2)  # 用.urlopen打开上一步返回的结果，得到请求后的响应内容

apicontent = response.read()  #将响应内容用read()读取出来

print  apicontent  #打印读取到的内容