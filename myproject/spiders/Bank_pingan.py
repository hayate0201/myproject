# -*- coding: utf-8 -*-
# 平安银行

import scrapy,json,codecs,time,os,math,collections,re
from myproject.items import MyprojectItem
class PinganSpider(scrapy.spiders.Spider):

    name = "bank_pingan"
    allowed_domains = ["haoshi.pingan.com/"]
    start_urls=[
        'http://licai.pingan.com/licai.shtml?templateType=yinHangLiCai']
    
    #自定义管道
    custom_settings = {
        'ITEM_PIPELINES':{
            'myproject.pip.pipelines_pingan.PinganPipeline': 1,
            'myproject.pipelines.Pipelines': 100,
            'myproject.pip.pipelines_mongo.MongodbPipeline': 200
        }
    }
    
    def __init__(self):
        self.page=1
        self.row=1
        
    def parse(self, response):
        #获取页码
        total = response.xpath('normalize-space(//*[@id="list_left"]/div[1]/div[3]/span/b/text())').extract()[0]
        total = float(total)
        page = int(math.ceil(total/10.0)) #这里默认是10条为1页

        for i in range(0,page):
            i += 1 
            urls = "http://licai.pingan.com/licai.shtml?templateType=yinHangLiCai&npage=%s" %i
            yield scrapy.Request(urls, callback=self.get_url,dont_filter=True)
    def get_url(self,response):
        sites = response.xpath('//div[@class="pl_conS"]/dl')
        for i in sites:
            href = i.xpath('dt/span/a/@href').extract()[0]
            url = re.search('licaichanpin',href,re.M|re.I)
            openFlag = i.xpath('dd/ul/input[@name="openFlag"]/@value').extract()[0]
            if url and openFlag == "0":
                urls = "http://licai.pingan.com"+href
                yield scrapy.Request(urls, callback=self.get_json,dont_filter=True)

    def get_json(self,response):
        #URL
        url = response.url.split("/")[-1]
        code = url[0:-6]

        item = MyprojectItem()
        item = collections.OrderedDict(item)
        item['bank_code']   = "pingan"#银行编码
        item['bank_name']   = "平安银行"#银行名称
        item['bank_type']   = "1"#银行类型：
        item['prod_code']   = code#产品编码
        item['prod_name']   = response.xpath('//div[@class="title"]/span[@class="cor_1"]/text()').extract()[0]
        item['prod_type']   = response.xpath('normalize-space(//table[@class="detail_tab3"]/tbody/tr[5]/td[4]/text())').extract()[0]#产品类型
        item['start_amount']= response.xpath('normalize-space(//table[@class="detail_tab3"]/tbody/tr[4]/td[2]/text())').extract()#起购金额
        item['coin_type']   = response.xpath('normalize-space(//table[@class="detail_tab3"]/tbody/tr[3]/td[4]/text())').extract()#货币类型
        item['live_time']   = response.xpath('normalize-space(//table[@class="detail_tab3"]/tbody/tr[3]/td[2]/text())').extract()#ProdLimit周期
        item['buying_start']= response.xpath('normalize-space(//table[@class="detail_tab3"]/tbody/tr[1]/td[2]/text())').extract()
        item['buying_end']  = response.xpath('normalize-space(//table[@class="detail_tab3"]/tbody/tr[1]/td[4]/text())').extract()
        item['std_rate']    = response.xpath('normalize-space(//table[@class="detail_tab3"]/tbody/tr[5]/td[2]/text())').extract()#ProdProfit利率
        item['risk_level']  = response.xpath('normalize-space(/html/body/div[8]/div[2]/p[1]/span[3]/text())').extract()[0]#风险等级
        item['status']      = response.xpath('normalize-space(//div[@class="top"]/p/span[2]/text())').extract()
        item['create_time'] = time.time()#抓取时间
        item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
        #进入管道进行过滤
        yield item