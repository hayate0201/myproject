# -*- coding: utf-8 -*-
# 交通银行

import scrapy,json,codecs,time,os,collections,re
from myproject.items import MyprojectItem
class BankcommSpider(scrapy.spiders.Spider):

    name = "bank_comm"
    allowed_domains = ["www.bankcomm.com/"]
    start_urls=[
        'http://www.bankcomm.com/BankCommSite/jyjr/cn/lcpd/queryFundInfoListNew.do?currency=-1' #-1全部 1人民币 2外币
        ]
        
    #自定义管道
    custom_settings = {
        'ITEM_PIPELINES':{
            'myproject.pipelines.Pipelines': 100,
            'myproject.pip.pipelines_mongo.MongodbPipeline': 200
        }
    }
    
    def __init__(self):
        self.page=1
        self.row=1

    def parse(self, response):
        sites = response.xpath('//div[@class="lc-conter-main"]/div/ul/li')
        
        for site in sites:
            code = site.xpath('@id').extract()[0] #产品编号
        #code = "0191150020"
        #code = "0131150001"
            urls = "http://www.bankcomm.com/BankCommSite/jyjr/cn/lcpd/queryFundInfoNew.do?code=%s" %code
            yield scrapy.Request(urls,callback=self.getjson,dont_filter=True)
        
        
        #yield scrapy.Request(urls,callback=self.getjson,dont_filter=True)
    def getjson(self,response):
        
        i = response.xpath('//div[@class="main"]//table/tr/td[1]/text()')
        code = i[1].extract()
        item = MyprojectItem()
        item = collections.OrderedDict(item)
        item['bank_code']   = "BOC"#银行编码
        item['bank_name']   = "交通银行"#银行名称
        item['bank_type']   = "1"#银行类型：
        item['prod_code']   = i[1].extract().strip()#产品编码
        item['prod_name']   = i[0].extract().strip()#产品名称
        item['prod_type']   = ""#产品类型
        item['live_time']   = ""
        item['buying_start']= ""
        item['buying_end']  = ""
        #ProdProfit利率
        if code == '02':
            item['std_rate']    = ""
            
        elif code[0:1] == '2':
            item['std_rate']    = i[10].extract().strip()
            item['live_time']   = i[8].extract()[0]#ProdLimit周期
            item['buying_start']= i[6].extract()[0]
            item['buying_end']  = i[7].extract()[0]
            item['prod_type']   = "封闭式"#产品类型
        else:
            #item['std_rate']    = i[7].extract().strip()
            item['std_rate']    = re.findall(r'(\d*.\d*%)',i[7].extract().strip(),re.M)
            if item['std_rate'] != []:
                item['std_rate'] = item['std_rate'][0]
            else:
                item['std_rate'] = ""
            item['prod_type']   = "开放式"#产品类型
            
        item['start_amount']= i[4].extract().strip()
        item['risk_level']  = i[3].extract().strip()#风险等级
        
        item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
        
        yield item
        