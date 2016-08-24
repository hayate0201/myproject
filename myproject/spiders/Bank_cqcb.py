# -*- coding: utf-8 -*-
# 重庆银行

import scrapy,json,codecs,time,os,collections,datetime
from myproject.items import MyprojectItem
class BankabcSpider(scrapy.spiders.Spider):
    name = "bank_cqcb"
    allowed_domains = ["www.cqcbank.com"]
    start_urls=[
        'http://www.cqcbank.com/portal/zh_CN/personal/lczq/cjxllcp/lcfxgg/index.html',
    ]
    #自定义管道
    custom_settings = {
        'ITEM_PIPELINES':{
            'myproject.pip.pipelines_cqcb.CqcbPipeline': 1,
            'myproject.pipelines.Pipelines': 100,
            'myproject.pip.pipelines_mongo.MongodbPipeline': 200
        }
    }
    def __init__(self):
        self.page=1
        self.row=1
        
    def parse(self, response):
        #读取当前页文章
        sites = response.xpath('//div[@class="cq_dt_box4"]/ul/li')
        for site in sites:
            url  = site.xpath('a/@href').extract()[0]
            urls = "http://www.cqcbank.com%s" %url
            print urls
            yield scrapy.Request(urls,callback=self.get_data,dont_filter=True)
            
            #yield scrapy.Request(urls, callback=self.get_data,body=str(obj))

        

    def get_data(self,response):
        
        sites = response.xpath('//td[@class="ZW"]/table[1]/tbody/tr')
        for i in sites:
            item = MyprojectItem()
            item = collections.OrderedDict(item)
            TD1 = i.xpath('td[1]/p')
            x=[]
            for n in TD1:
                title = n.xpath('span//text()').extract()
                x.append("".join(title))
            #print order
            #print x
            item['bank_code']   = "cqcb"#银行编码
            item['bank_name']   = "重庆银行"#银行名称
            item['bank_type']   = "1"#银行类型
            item['prod_code']   = ""#产品编码
            #print u"产品名字"
            item['prod_name']   = x[0] if x else ""#产品名称
            time = "".join(i.xpath('td[2]/p//text()').extract()).encode("GBK", "ignore").replace(" ","")
            #print u"时间"
            item['buying_start']= time.split("-")
            item['buying_end']  = time.split("-")
            item['prod_type']   = ""
            item['start_amount']= 50000
            item['coin_type']   = "人民币"
            #print u"周期"
            item['live_time']   = "".join(i.xpath('td[4]/p//text()').extract())
            item['std_rate']    = "".join(i.xpath('td[5]/p//text()').extract())
            item['risk_level']  = "".join(i.xpath('td[3]/p//text()').extract())
            yield item