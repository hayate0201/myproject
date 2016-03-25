# -*- coding: utf-8 -*-
import scrapy
import time
'''
class AbcSpider(scrapy.Spider):
    name = "abc"
    allowed_domains = ["abchina.com.cn"]
    page=1
    start_urls=[]
    for page in range(1,100):
        start_urls.append('http://ewealth.abchina.com/app/data/api/DataService/BoeProductV2?i=1&s=10&o=0' %page)

    def parse(self, response):
        filename = response.url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.body)
'''

