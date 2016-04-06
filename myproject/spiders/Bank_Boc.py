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
        
        BASE_PATH = os.getcwd()
        self.dir = os.path.join(BASE_PATH,"myproject/data/boc.json")
        self.file = codecs.open(self.dir, 'wb+', encoding='utf-8')
        self.file.write("")#清空文件内容
        
    def parse(self, response):
        #保存文件路径
        self.file = codecs.open(self.dir, 'a', encoding='utf-8')
        
        sites = response.xpath('//table/tbody')
        order = 1
        for tbody in sites:
            site = tbody.xpath('tr')
            for i in site:
                item = MyprojectItem()
                item['bank_code']   = "boc"#银行编码
                item['bank_name']   = "中国银行"#银行名称
                item['bank_type']   = "1"#银行类型
                item['prod_code']   = i.xpath('td[1]/text()').extract()[0]
                item['prod_name']   = i.xpath('td[2]/text()').extract()[0]
                item['prod_type']   = ""
                
                if order == 2:
                    item['live_time']   = i.xpath('td[4]/text()').extract()[0]
                    item['start_amount']= i.xpath('td[6]/text()').extract()[0]
                    item['risk_level']  = i.xpath('td[12]/text()').extract()[0]#风险等级
                else:
                    item['live_time']   = i.xpath('td[3]/text()').extract()[0]
                    item['start_amount']= i.xpath('td[5]/text()').extract()[0]
                    item['risk_level']  = i.xpath('td[11]/text()').extract()[0]#风险等级
                item['std_rate']    = i.xpath('td[4]/text()').extract()[0]
               
                item['create_time'] = time.time()#抓取时间
                item['total_type']  = "json"#全部数据类型
                
                line = json.dumps(dict(item)) + '\n'
                self.file.write(line.decode("unicode_escape")) 
            order +=1