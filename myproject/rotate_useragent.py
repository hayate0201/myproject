# -*-coding:utf-8-*-  
  
import random  
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware  
  
class RotateUserAgentMiddleware(UserAgentMiddleware):  
  
    def __init__(self, user_agent=''):  
        self.user_agent = user_agent  
  
    def process_request(self, request, spider):  
        ua = random.choice(self.user_agent_list)  
        if ua:  
            #显示当前使用的useragent  
            print "********Current UserAgent:%s************" %ua  
  
            #记录  
            #log.msg('Current UserAgent: '+ua, level='INFO')  
            request.headers.setdefault('User-Agent', ua)  
  
    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape  
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php  
    user_agent_list = [  
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"
       ]  