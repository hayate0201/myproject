# -*- coding: utf-8 -*-
# 宁波银行

import scrapy,json,codecs,time,os,re
from myproject.items import MyprojectItem

class nbcbSpider(scrapy.spiders.Spider):
    name = "bank_nbcb"
    allowed_domains = ["http://directbank.cib.com.cn/"]
    start_urls=['http://www.nbcb.com.cn/wealth_management_center/financial/index.shtml']
    
    def __init__(self):

        #文件设置
        BASE_PATH = os.getcwd()
        dirname = os.path.join(BASE_PATH,"data")
        if not os.path.exists(dirname):
			os.makedirs(dirname)
        self.dir = os.path.join(dirname,self.name+".json")
        self.file = codecs.open(self.dir, 'wb+', encoding='utf-8')
        self.file.write("")#清空文件内容
    
    def parse(self, response):
        #保存文件路径
        self.file = codecs.open(self.dir, 'a+', encoding='utf-8')
        
        #获取总页码
        text = str(response.body)
        test = re.findall(r'pageCount:(\d+)',text,re.M)
        totalPage = int(test[0])
        
        for i in range(0,totalPage):
            if i == 0:
                urls = "http://www.nbcb.com.cn/wealth_management_center/financial/index.shtml"
            else:
                urls = "http://www.nbcb.com.cn/wealth_management_center/financial/index_%d.shtml" %i
            yield scrapy.Request(urls, callback=self.get_url,dont_filter=True)
        
        #urls = 'http://www.nbcb.com.cn/wealth_management_center/financial/wealth_products_series/huitian_benefits/201603/t20160331_910256.shtml'
        #yield scrapy.Request(urls, callback=self.get_json,dont_filter=True)
    def get_url(self,response):
        #提取区域
        sites = response.xpath('//table[@id="tbl_wealth_saling"]/tbody[@class="tbody"]/tr')
        for i in sites:
            urls = i.xpath('td[2]/a/@href').extract()[0]
            yield scrapy.Request(urls, callback=self.get_json,dont_filter=True)
        
    def get_json(self,response):
        #URL
        sites = response.xpath('//table[@id="tbl_wealth_product"]/tbody/tr')
        item = MyprojectItem()
        item['bank_code']   = "NBCB"#银行编码
        item['bank_name']   = "宁波银行"#银行名称
        item['bank_type']   = "1"#银行类型：
        item['prod_code']   = sites[0].xpath('td[2]/text()').extract()[0]#产品编码
        item['prod_name']   = response.xpath('normalize-space(//*[@id="wealth_product"]/div[1]/ul/li/span/text())').extract()[0]#产品名称
        item['prod_type']   = "1"#产品类型
        item['start_amount']= sites[4].xpath('td[2]/text()').extract()[0]
        item['live_time']   = sites[1].xpath('td[4]/text()').extract()[0]
        rate = sites[5].xpath('td[2]/text()').extract()[0]
        item['std_rate'] = re.findall(r'(\d+.\d+%)',rate,re.M)
        item['risk_level']  = sites[6].xpath('td[4]/text()').extract()[0]
        item['create_time'] = time.time()#抓取时间
        item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
        item['total_data']  = ""#全部数据
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode("unicode_escape")) 