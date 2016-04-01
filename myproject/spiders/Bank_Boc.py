# -*- coding: utf-8 -*-
# 中国银行

import scrapy,json,codecs,time,os
from myproject.items import MyprojectItem
class BocSpider(scrapy.spiders.Spider):

    name = "boc"
    allowed_domains = ["www.boc.cn"]
    start_urls=[
        'http://www.boc.cn/fimarkets/cs8/201109/t20110922_1532694.html']
    
    def __init__(self):
        self.page=1
        self.row=1
        BASE_PATH = os.getcwd()
        self.dir = os.path.join(BASE_PATH,"myproject/data/boc.json")
        self.file = codecs.open(self.dir, 'wb+', encoding='utf-8')
        self.file.write("")#清空文件内容
        
    def parse(self, response):
        #保存文件路径
        self.file = codecs.open(self.dir, 'a', encoding='utf-8')
