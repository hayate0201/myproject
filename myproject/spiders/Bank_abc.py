# -*- coding: utf-8 -*-
# 农业银行

import scrapy,json,codecs,time,os,collections,datetime
from myproject.items import MyprojectItem
class BankabcSpider(scrapy.spiders.Spider):
    name = "bank_abc"
    allowed_domains = ["ewealth.abchina.com"]
    start_urls=[
        'http://ewealth.abchina.com/app/data/api/DataService/BoeProductV2?i=1&s=15&o=0&w=%E5%8F%AF%E5%94%AE|||||||1||0||',
        #'http://ewealth.abchina.com/fs/AD162013.htm'
    ]
    #自定义管道
    custom_settings = {
        'ITEM_PIPELINES':{
            'myproject.pip.pipelines_abc.AbcPipeline': 1,
            'myproject.pipelines.Pipelines': 100,
            'myproject.pip.pipelines_mongo.MongodbPipeline': 200
        }
    }
    def __init__(self):
        self.page=1
        self.row=1
        
    def parse(self, response):
        #产品总数目
        sel = scrapy.Selector(response)
        total = sel.xpath('//Table1/total/text()').extract()[0] 
        total = int(total) #转为整数方便做比较
        
        print total
        sites = response.xpath('//NewDataSet/Table')
        for site in sites:
            obj = {}
            obj['prod_code']  = site.xpath('ProductNo/text()').extract()[0]#产品编码
            obj['start_amount'] = site.xpath('PurStarAmo/text()').extract()[0]
            urls  = "http://ewealth.abchina.com/fs/"+str(obj['prod_code'])+".htm"
            self.row += 1
            yield scrapy.Request(urls, callback=self.get_data,body=str(obj))
         
        self.page += 1
        urls = 'http://ewealth.abchina.com/app/data/api/DataService/BoeProductV2?i=%d&s=15&o=0&w=可售|||||||1||0||' %self.page
        
        try:
            if self.row < total:
                #print "正在读取...."
                yield scrapy.Request(urls, callback=self.parse)
        except:
            print "This Error"
        

    def get_data(self,response):
        obj = eval(response.request.body)
        site = response.xpath('//table')
        item = MyprojectItem()
        item = collections.OrderedDict(item)
        item['bank_code']   = "abc"#银行编码
        item['bank_name']   = "农业银行"#银行名称
        item['prod_code']   = obj['prod_code']#产品编码
        item['prod_name']   = response.xpath('/html/body/div[4]/div[1]/text()').extract()[0]#产品名称
        item['prod_type']   = site.xpath('tr[14]/td[2]/text()').extract()[0]#产品类型
        
        item['start_amount']= obj['start_amount']#起购金额
        item['coin_type']   = site.xpath('tr[4]/td[2]/text()').extract()[0]#货币类型
        item['live_time']   = site.xpath('tr[10]/td[1]/text()').extract()[0]#ProdLimit周期
        item['buying_start']= site.xpath('tr[6]/td[1]/text()').extract()[0]
        item['buying_end']  = site.xpath('tr[6]/td[2]/text()').extract()[0]
        item['std_rate']    = site.xpath('tr[10]/td[2]/text()').extract()[0]#ProdProfit利率
        item['risk_level']  = site.xpath('tr[14]/td[1]/text()').extract()[0]
        
        yield item