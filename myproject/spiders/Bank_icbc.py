# -*- coding: utf-8 -*-
# 工商银行

import scrapy,json,codecs,time,os
from myproject.items import MyprojectItem
class IcbcSpider(scrapy.spiders.Spider):

    name = "icbc"
    allowed_domains = ["icbc.com.cn"]
    start_urls=[
        'http://www.icbc.com.cn/ICBCDynamicSite2/money/moneytabs.htm']
    
    def __init__(self):
        self.page=1
        self.row=1
        BASE_PATH = os.getcwd()
        self.dir = os.path.join(BASE_PATH,"myproject/data/icbc.json")
        self.file = codecs.open(self.dir, 'wb+', encoding='utf-8')
        self.file.write("")#清空文件内容
        
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
        #文件打开方式为添加
        self.file = codecs.open(self.dir, 'a', encoding='utf-8')
        
        #转为JOSN格式
        json_obj=json.loads(response.body) 
        
        for i in json_obj:
            item = MyprojectItem()
            item['bank_code']   = "ICBC"#银行编码
            item['bank_name']   = "工商银行"#银行名称
            item['bank_type']   = "1"#银行类型：
            item['prod_code']   = i['prodID']#产品编码
            item['prod_name']   = i['productName']#产品名称
            item['prod_type']   = i['categoryL1']#产品类型
            item['start_amount']= i['buyPaamt']#起购金额
            item['live_time']   = i['productTerm']#ProdLimit周期
            item['std_rate']    = i['intendYield']#ProdProfit利率
            item['risk_level']  = 1#风险等级
            item['create_time'] = time.time()#抓取时间
            item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
            
            line = json.dumps(dict(item)) + '\n'
            self.file.write(line.decode("unicode_escape")) 
        