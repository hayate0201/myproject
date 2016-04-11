# -*- coding: utf-8 -*-
# 平安银行

import scrapy,json,codecs,time,os,math,collections
from myproject.items import MyprojectItem
class PinganSpider(scrapy.spiders.Spider):

    name = "bank_pingan"
    allowed_domains = ["haoshi.pingan.com/"]
    start_urls=[
        'http://chaoshi.pingan.com/bankListIframe.shtml?npage=1']
    
    def __init__(self):
        self.page=1
        self.row=1
        
    def parse(self, response):
        
        #获取页码
        total = response.xpath('/html/body/div/div[2]/span/font/text()').extract()[0]
        total = float(total)
        page = int(math.ceil(total/10)) #这里默认是10条为1页
        
        for i in range(0,page):
            i += 1 
            urls = "http://chaoshi.pingan.com/bankListIframe.shtml?npage=%s" %i
            yield scrapy.Request(urls, callback=self.get_url,dont_filter=True)

    def get_url(self,response):
        sites = response.xpath('//div[@class="search_list_box"]/div/h1')
        for site in sites:
            item = site.xpath('a[@onclick]/@onclick').extract()[0]
            urls = item[11:(len(item)-2)]
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
        item['prod_name']   = response.xpath('//div[@class="title"]/span[@class="cor_1"]/text()').extract()
        item['prod_type']   = ""#产品类型
        item['start_amount']= response.xpath('normalize-space(//table[@class="detail_tab3"]/tbody/tr[4]/td[2]/text())').extract()#起购金额
        item['live_time']   = response.xpath('normalize-space(//table[@class="detail_tab3"]/tbody/tr[3]/td[2]/text())').extract()#ProdLimit周期
        item['std_rate']    = response.xpath('normalize-space(//table[@class="detail_tab3"]/tbody/tr[5]/td[2]/text())').extract()#ProdProfit利率
        item['risk_level']  = ""#风险等级
        item['status']      = response.xpath('normalize-space(//div[@class="top"]/p/span[2]/text())').extract()
        item['create_time'] = time.time()#抓取时间
        item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
        #进入管道进行过滤
        yield item