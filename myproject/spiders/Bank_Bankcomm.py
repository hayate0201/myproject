# -*- coding: utf-8 -*-
# 交通银行

import scrapy,json,codecs,time,os,collections
from myproject.items import MyprojectItem
class BankcommSpider(scrapy.spiders.Spider):

    name = "bank_comm"
    allowed_domains = ["www.bankcomm.com/"]
    start_urls=[
        'http://www.bankcomm.com/BankCommSite/jyjr/cn/lcpd/queryFundInfoListNew.do?currency=-1' #-1全部 1人民币 2外币
        ]
        
    
    def __init__(self):
        self.page=1
        self.row=1

    def parse(self, response):
        sites = response.xpath('//div[@class="lc-conter-main"]/div/ul/li')
        
        for site in sites:
            code = site.xpath('@id').extract()[0] #产品编号
            urls = "http://www.bankcomm.com/BankCommSite/jyjr/cn/lcpd/queryFundInfoNew.do?code=%s" %code
            yield scrapy.Request(urls,callback=self.getjson,dont_filter=True)
        
        
        #yield scrapy.Request(urls,callback=self.getjson,dont_filter=True)
    def getjson(self,response):
        print "GET JSON"
        code = response.url.split("/")[-1]
        code = code[25:len(code)]
        print code
        code = code[0:2]
        print code
        
        i = response.xpath('//div[@class="main"]//table/tr/td[1]/text()')
        item = MyprojectItem()
        item = collections.OrderedDict(item)
        item['bank_code']   = "BOC"#银行编码
        item['bank_name']   = "交通银行"#银行名称
        item['bank_type']   = "1"#银行类型：
        item['prod_code']   = i[1].extract().strip()#产品编码
        item['prod_name']   = i[0].extract().strip()#产品名称
        item['prod_type']   = ""#产品类型
        
        item['live_time']   = ""#ProdLimit周期
        #ProdProfit利率
        if code == '02':
            item['std_rate']    = ""
        elif code[0:1] == '2':
            item['std_rate']    = i[10].extract().strip()
        else:
            item['std_rate']    = i[7].extract().strip()
            
        item['start_amount']= i[4].extract().strip()
        item['risk_level']  = i[3].extract().strip()#风险等级
        item['create_time'] = time.time()#抓取时间
        item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
        
        yield item