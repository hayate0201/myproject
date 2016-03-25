# -*- coding: utf-8 -*-
from scrapy.spiders import  XMLFeedSpider
from myproject.items import MyprojectItem
import time

class AbcSpider(XMLFeedSpider):
    name = "abc"
    allowed_domains = ["abchina.com.cn"]
    page=1
    start_urls=['http://ewealth.abchina.com/app/data/api/DataService/BoeProductV2?i=%s&s=10&o=0' %page]
    iterator = 'NewDataSet'
    itertag = 'NewDataSet'
    def parse(self, response,node):
        item = MyprojectItem()
        item['id'] = node.xpath('@id').extract()
        item['name'] = node.xpath('name').extract()
        item['description'] = node.xpath('description').extract()
        return item

    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

    #获取当前时间
    def getCurrentDate(self):
        return time.strftime('%Y-%m-%d',time.localtime(time.time()))
    #写入日志
    #f_handler=open('out.log', 'w')
    #sys.stdout=f_handler/.,m