#coding=utf8
__author__ = 'apple'

import urllib
import urllib2
import cookielib
import time
start=time.clock()
#cookie文件存储地址
filename = 'cookie.txt'
#cookie实例生成,基于CookieJar对象实例
#cookie=cookielib.CookieJar()
cookie=cookielib.MozillaCookieJar(filename)
#利用urllib2库里的HttpCookieProcessor对象来创建cookie处理器
handler=urllib2.HTTPCookieProcessor(cookie)
#通过handler来构建opener
opener=urllib2.build_opener(handler)
values={"account":"admin","password":"nydbnydb"}
data=urllib.urlencode(values)
#loginUrl="http://demo.hitudi.net:81/Admin/index.php/Index/index/"
loginUrl="http://demo.hitudi.net:81/Admin/index.php/Public/signin"
#模拟登陆，将cookie保存到变量
result = opener.open(loginUrl,data)
#保存cookie到cookie文件中
cookie.save(ignore_discard=True,ignore_expires=True)
#利用cookie去请求另一个系统内地址
indexUrl="http://demo.hitudi.net:81/Admin/index.php/Index/index/"
result=opener.open(indexUrl)
print result.read()
'''
request = urllib2.Request(loginUrl,data)
try:
    response = urllib2.urlopen(request)
    print response.read()

except urllib2.HTTPError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
else:
    print "OK"
'''
end=time.clock()
print("read: %f s"%(end-start))