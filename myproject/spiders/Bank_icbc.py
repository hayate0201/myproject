# -*- coding: utf-8 -*-
# 工商银行

import scrapy,json,codecs,time,os,collections
from myproject.items import MyprojectItem
class IcbcSpider(scrapy.spiders.Spider):

    name = "bank_icbc"
    allowed_domains = ["icbc.com.cn"]
    start_urls=[
        'http://www.icbc.com.cn/ICBCDynamicSite2/money/moneytabs.htm']
    
    #自定义管道
    custom_settings = {
        'ITEM_PIPELINES':{
            'myproject.pip.pipelines_icbc.IcbcPipeline': 1,
            'myproject.pipelines.Pipelines': 100,
            'myproject.pip.pipelines_mongo.MongodbPipeline': 200
        }
    }
    
    def __init__(self):
        self.page=1
        self.row=1

    def parse(self, response):
        
        sites = response.xpath('//div[@data-catal2]')
        i = 1
        items = []
        for site in sites:
            item = {}
            item['name'] =site.xpath('normalize-space(text())').extract()
            item['cata'] = site.xpath('@data-cata').extract()[0]
            item['catal2']= site.xpath('@data-catal2').extract()[0]
            items.append(item)
        
        
        for x in items:
            #print x['cate']
            urls = "http://www.icbc.com.cn/ICBCDynamicSite2/money/services/MoenyListService.ashx?ctl1=%s&ctl2=%s" %(x['cata'],x['catal2'])
            print "Start GET JSON: ctl1=%s ctl2=%s" %(x['cata'],x['catal2'])
            yield scrapy.Request(urls,callback=self.getjson)
        
        
        
    def getjson(self,response):
        #转为JOSN格式
        json_obj=json.loads(response.body) 
        for i in json_obj:
            item = MyprojectItem()
            item = collections.OrderedDict(item)
            item['bank_code']   = "icbc"#银行编码
            item['bank_name']   = "工商银行"#银行名称
            item['bank_type']   = "1"#银行类型：
            item['prod_code']   = i['prodID']#产品编码
            item['prod_name']   = i['productName']#产品名称
            item['prod_type']   = "非保本浮动收益型"#产品类型
            item['start_amount']= i['buyPaamt']#起购金额
            item['live_time']   = i['productTerm']#ProdLimit周期
            time = i['offerPeriod'].split("-")
            item['buying_start']= time[0]
            item['buying_end']  = time[1]
            item['std_rate']    = i['intendYield']#ProdProfit利率
            item['risk_level']  = ""#风险等级
            item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
 
            yield item
        