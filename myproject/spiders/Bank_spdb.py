# -*- coding: utf-8 -*-
# 浦发银行
# 产品表单样式多，规律不统一，采集有问题

import scrapy,json,codecs,time,os,re,chardet,collections
from myproject.items import MyprojectItem
class SpdbSpider(scrapy.spiders.Spider):
    name = "spdb"
    allowed_domains = ["http://ebank.spdb.com.cn/"]
    start_urls=[
        'http://ebank.spdb.com.cn/net/finnaceMoreInfo.do?ftype=7&num=11&ispage=1&_PagableInfor.PageNo=1']
    
    def __init__(self):
        self.page=1
        self.type=0
        self.typelist=[7,0,5,3,2]

    def parse(self, response):
        #循环系列
        
        for i in self.typelist:
            self.type = i
            urls = 'http://ebank.spdb.com.cn/net/finnaceMoreInfo.do?ftype=%d&num=11&ispage=1&_PagableInfor.PageNo=1' %i
            print urls
            yield scrapy.Request(urls, callback=self.get_urllist,dont_filter=True)
        
        #urls = 'http://ebank.spdb.com.cn/net/www/20160329/per_0000900993.html'
        #yield scrapy.Request(urls, callback=self.get_json,dont_filter=True)
        #urls = 'http://ebank.spdb.com.cn/net/finnaceMoreInfo.do?ftype=7&num=11&ispage=1&_PagableInfor.PageNo=1'
        #yield scrapy.Request(urls, callback=self.get_urllist,dont_filter=True)
    def get_urllist(self,response):
        #每个系列的页码
        
        page = response.xpath('//*[@id="pagelist"]/span[2]/text()').extract()
        if not page:
            maxpage = 1
        else:
            test = re.findall(r'/(\d*)',page[0],re.M)
            maxpage = int(test[0])
        for i in range(0,maxpage):
            page = i+1
            urls = 'http://ebank.spdb.com.cn/net/finnaceMoreInfo.do?ftype=%d&num=11&ispage=1&_PagableInfor.PageNo=%d' %(self.type,page)
            print urls
            yield scrapy.Request(urls, callback=self.get_itemurl,dont_filter=True)
        '''
        urls = 'http://ebank.spdb.com.cn/net/finnaceMoreInfo.do?ftype=7&num=11&ispage=1&_PagableInfor.PageNo=1'
        yield scrapy.Request(urls, callback=self.get_itemurl,dont_filter=True)
        '''
    def get_itemurl(self,response):
        sites = response.xpath('//table/tr')
        
        for i in sites:
            site =  i.xpath('td[@class="border0"]/a/@href').extract()
            commit = i.xpath('normalize-space(td[6]//text())').extract()[0]
            if commit != "-" and site !=[]:
                url = 'http://ebank.spdb.com.cn'+site[0]
                print url
                yield scrapy.Request(url, callback=self.get_json,dont_filter=True)
            
    def get_json(self,response):
        body = str(response.body)
        content_type = chardet.detect(body)
        
        if content_type['encoding'] != "UTF-8":
            body = body.decode(content_type['encoding'])
        body = body.encode("utf-8")
        
        
        item = MyprojectItem()
        item = collections.OrderedDict(item)
        item['bank_code']   = "spdb"#银行编码
        item['bank_name']   = "浦发银行"#银行名称
        item['bank_type']   = "1"#银行类型：
        item['prod_code']   = re.findall(r'([0-9]{10})',body)[0]#产品编码
        item['prod_name']   = response.xpath('//table/tbody/tr[1]/td[2]/p/text()').extract()[0]
        
        zz = u'产品类型'
        item['prod_type']   = response.xpath("//td[p[text()='%s']]/following-sibling::*/p/text()" %(zz)).extract()[0]#产品类型
        item['live_time']   = ""
        item['std_rate']    = ""
        zz = u'投资者认购金额'
        item['start_amount'] = response.xpath("//td[p[text()='%s']]/following-sibling::*/p/text()" %(zz)).extract()[0]
        
        zz = [u'产品风险等级',u'风险评定']
        risk_level = response.xpath("//td[p[text()='%s']] |//td[p[text()='%s']] " %(zz[0],zz[1]))
        item['risk_level'] = risk_level.xpath('following-sibling::*/p/text()').extract()
        item['create_time'] = time.time()#抓取时间
        item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
        
        yield item