# -*- coding: utf-8 -*-
# 中国银行

import scrapy,json,codecs,time,os,collections
from myproject.items import MyprojectItem


class BocSpider(scrapy.spiders.Spider):
    name = "bank_boc"
    allowed_domains = ["www.boc.cn"]
    start_urls=[
        'http://www.boc.cn/fimarkets/cs8/201109/t20110922_1532694.html']
        
    #自定义管道
    '''
    custom_settings = {
        'ITEM_PIPELINES':{'myproject.pip.pipelines_1.CustomPipeline': 200}
    }
    '''
  
    def parse(self, response):
        sites = response.xpath('//table/tbody')
        order = 1
        for tbody in sites:
            site = tbody.xpath('tr')
            item = MyprojectItem()
            item = collections.OrderedDict(item)
            for i in site:
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
                
                yield item
            order +=1