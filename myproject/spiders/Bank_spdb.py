# -*- coding: utf-8 -*-
# 浦发银行
# 产品表单样式多，规律不统一，采集有问题

import scrapy,json,codecs,time,os,re,chardet,collections
from myproject.items import MyprojectItem
from scrapy.exceptions import DropItem
class SpdbSpider(scrapy.spiders.Spider):
    name = "bank_spdb"
    allowed_domains = ["http://per.spdb.com.cn/"]
    start_urls=[
        'http://per.spdb.com.cn/bank_financing/financial_product/'
        ]
    
    #自定义管道
    custom_settings = {
        'ITEM_PIPELINES':{
            'myproject.pip.pipelines_spdb.SpdbPipeline': 1,
            'myproject.pipelines.Pipelines': 100,
            'myproject.pip.pipelines_mongo.MongodbPipeline': 200
        }
    }
    
    def __init__(self):
        self.page=1
        self.maxpage=1
        self.ids_seen = set()
        
    def parse(self, response):

        urls = "http://per.spdb.com.cn/was5/web/search"
        print "================START_REQUESTS============"
        #进行POST请求，提交相关参数
        yield scrapy.FormRequest(
            urls,
            formdata = {
                'page':'1',
                'metadata':'finance_no|finance_state|finance_allname|finance_income|FINANCE_LIMITTIME|finance_buylimitmoney|finance_anticipate|finance_buydate|finance_stopdate|Finance_limittime_type|docpuburl',
                'channelid':'298687',
                'searchword':u'(%)*(Finance_limittime_type=%)*(finance_state=%)*(finance_buylimitmoney=%)\
                            *(finance_state=可购买)*(chnlid=879)',
                }, 
            callback = self.get_code,
            dont_filter=True
        )
        
    def get_code(self,response):
        print response.url
        body = eval(response.body)
        
        self.maxpage = int(body['pageTotal'])
        print body['pageIndex']
        for i in body['rows']:
            prod_code  = i['finance_no']#产品编码
            if prod_code in self.ids_seen:
                print "Having!!"
            else:
                self.ids_seen.add(prod_code)
                #print prod_code+"   "+i['finance_allname']
                urls = "https://ebank.spdb.com.cn/nbper/PreBankFinanceBuy.do?FinanceNo="+prod_code
                yield scrapy.Request(urls,callback=self.get_data,dont_filter=True)
        if self.page < self.maxpage:
            self.page += 1
            urls = "http://per.spdb.com.cn/was5/web/search"
            yield scrapy.FormRequest(
            urls,
            formdata = {
                'page':'%d' %self.page,
                'metadata':'finance_no|finance_state|finance_allname|finance_income|FINANCE_LIMITTIME|finance_buylimitmoney|finance_anticipate|finance_buydate|finance_stopdate|Finance_limittime_type|docpuburl',
                'channelid':'298687',
                'searchword':u'(%)*(Finance_limittime_type=%)*(finance_state=%)*(finance_buylimitmoney=%)\
                            *(finance_state=可购买)*(chnlid=879)',
                }, 
            callback = self.get_code,
            dont_filter=True
        )
            
    def get_data(self,response): 
        item = MyprojectItem()
        item = collections.OrderedDict(item)
        
        item['bank_code']   = "spdb"
        item['bank_name']   = "浦发银行"
        item['bank_type']   = "1"

        prod_code   = response.xpath('/html/body/form/div[6]/div/div[2]/div[1]/div[2]/div/text()').extract()
        item['prod_code'] = prod_code[0] if prod_code else "" 
        
        prod_name   = response.xpath('/html/body/form/div[6]/div/div[2]/h4/text()').extract()
        item['prod_name']   = prod_name[0] if prod_name else "" 
        
        rule = [u'理财产品类型:',u'起点金额:',u'币种:',u'预期收益率:',u'申购起始日:',u'申购结束日:',
                u'产品期限:',u'风险等级:']
        field = ['prod_type','start_amount','coin_type','std_rate','buying_start','buying_end',
                'live_time','risk_level']
        order = 0
        for i in rule:
            spider = response.xpath("//div[text()='%s']/ancestor::td" %(i))
            data = spider.xpath('normalize-space(div[2]/div/text())').extract()
            item[field[order]] = data[0] if data else ""
            order += 1
            
        stauts = response.xpath('normalize-space(/html/body/form/div[8]/div/div/div/div/div/text())').extract()#产品状态
        item['stauts']  = stauts[0] if stauts else "0"
        
        item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
        if item['stauts'] == "":
            yield item
        else:
            print "Drop!!"