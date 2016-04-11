# -*- coding: utf-8 -*-
# 农业银行

import scrapy,json,codecs,time,os,collections
from myproject.items import MyprojectItem
class BankabcSpider(scrapy.spiders.Spider):
    name = "bank_abc"
    allowed_domains = ["ewealth.abchina.com"]
    start_urls=[
        'http://ewealth.abchina.com/app/data/api/DataService/BoeProductV2?i=1&s=15&o=0&w=%E5%8F%AF%E5%94%AE|||||||1||0||']
    
    def __init__(self):
        self.page=1
        self.row=1
        BASE_PATH = os.getcwd()
        dirname = os.path.join(BASE_PATH,"data")
        if not os.path.exists(dirname):
			os.makedirs(dirname)
        self.dir = os.path.join(dirname,self.name+".json")
        self.file = codecs.open(self.dir, 'wb+', encoding='utf-8')
        self.file.write("")#清空文件内容
        
    def parse(self, response):
        #产品总数目
        sel = scrapy.Selector(response)
        total = sel.xpath('//Table1/total/text()').extract()[0] 
        total = int(total,10) #转为整数方便做比较
        
        sites = response.xpath('//NewDataSet/Table')
        for site in sites:
            #定义Item
            item = MyprojectItem()
            item= collections.OrderedDict(item)
            item['bank_code']   = "abcbank"#银行编码
            item['bank_name']   = "农业银行"#银行名称
            item['bank_type']   = "1"#银行类型：
            item['prod_code']   = site.xpath('ProductNo/text()').extract()[0]#产品编码
            item['prod_name']   = site.xpath('ProdName/text()').extract()[0]#产品名称
            item['prod_type']   = "1"#产品类型
            item['start_amount']= site.xpath('PurStarAmo/text()').extract()[0]#起购金额
            item['live_time']   = site.xpath('ProdLimit/text()').extract()[0]#ProdLimit周期
            item['std_rate']    = site.xpath('ProdProfit/text()').extract()[0]#ProdProfit利率
            item['risk_level']  = ""#风险等级
            item['create_time'] = time.time()#抓取时间
            item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
            item['total_data']  = ""#全部数据
            
            #写入文件
            yield item
            self.row += 1
        self.page += 1
        urls = 'http://ewealth.abchina.com/app/data/api/DataService/BoeProductV2?i=%d&s=15&o=0&w=可售|||||||1||0||' %self.page
        
        try:
            if self.row < total:
                #print "正在读取...."
                yield scrapy.Request(urls, callback=self.parse)
        except:
            print "This Error"