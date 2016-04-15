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
        #self.typelist=[2]
        self.typelist=[7,0,5,2,3,1]
        
    def parse(self, response):
        #循环系列
        for i in self.typelist:
            self.type = i
            urls = 'http://ebank.spdb.com.cn/net/finnaceMoreInfo.do?ftype=%d&num=11&ispage=1&_PagableInfor.PageNo=1' %i
            yield scrapy.Request(urls, callback=self.get_itemurl,dont_filter=True)
        
        #urls = 'http://ebank.spdb.com.cn/net/www/20160329/per_0000900993.html'
        #yield scrapy.Request(urls, callback=self.get_json,dont_filter=True)
        #urls = 'http://ebank.spdb.com.cn/net/finnaceMoreInfo.do?ftype=7&num=11&ispage=1&_PagableInfor.PageNo=1'
        #yield scrapy.Request(urls, callback=self.get_urllist,dont_filter=True)

    def get_itemurl(self,response):
        sites = response.xpath('//table/tr')
        
        for i in sites:
            site =  i.xpath('td[@class="border0"]/a/@href').extract()
            commit = i.xpath('normalize-space(td[6]/div/text()|td[6]/text())').extract()[0]
            
            if commit != "-" and site !=[]:
                if commit == "":
                    commit = u"正在发行"
                    
                item = MyprojectItem()
                item['bank_code']   = "spdb"#银行编码
                item['bank_name']   = "浦发银行"#银行名称
                item['bank_type']   = ""#银行类型：
                item['prod_code']   = ""#产品编码     
                item['prod_name']   = i.xpath('td[1]/a/@title').extract()[0]
                item['prod_type']   = ""
                item['live_time']   = i.xpath('td[2]/text()').extract()[0]
                item['std_rate']    = i.xpath('td[3]/text()').extract()[0]
                item['start_amount']= ""
                time = i.xpath('td[5]/span/text()').extract()[0]
                time = time.split("-")
                item['buying_start']= time[0]
                item['buying_end']  = time[1]

                item['risk_level']  = ""
                item['status']      = commit
                item['total_type']  = "json"
                item = str(item)

                url = 'http://ebank.spdb.com.cn'+site[0]
                #print url
                yield scrapy.Request(url, callback=self.get_json,body=item,dont_filter=True)
            
    def get_json(self,response):
        #print response.request.body
        body = str(response.body)
        content_type = chardet.detect(body)
        if content_type['encoding'] != "UTF-8":
            body = body.decode(content_type['encoding'])
        body = body.encode("utf-8")
        prod_code   = re.findall(r'([0-9]{10})',body)[0]#产品编码
        item2 = eval(response.request.body)
        
        item = MyprojectItem()
        item = collections.OrderedDict(item)
        item['bank_code']   = item2['bank_code']
        item['bank_name']   = item2['bank_name']
        item['bank_type']   = item2['bank_type']
        item['prod_code']   = prod_code#产品编码     
        item['prod_name']   = item2['prod_name']
        item['prod_type']   = item2['prod_type']
        zz = u'产品类型'
        item['prod_type']   = response.xpath("//td[p[text()='%s']]/following-sibling::*/p/text()" %(zz)).extract()[0]#产品类型
        
        item['live_time']   = item2['live_time']
        item['std_rate']    = item2['std_rate']
        
        
        zz = [u'投资者认购金额',u'认购起点金额']
        start_amount = response.xpath("//td[p[text()='%s']]|//td[p[text()='%s']]" %(zz[0],zz[1]))
        item['start_amount']= start_amount.xpath('following-sibling::*/p/text()').extract()
        
        item['buying_start']= item2['buying_start']
        item['buying_end']  = item2['buying_end']
        
        zz = [u'产品风险等级',u'风险评定']
        risk_level = response.xpath("//td[p[text()='%s']] |//td[p[text()='%s']] " %(zz[0],zz[1]))
        item['risk_level'] = risk_level.xpath('following-sibling::*/p/text()').extract()
        item['total_type']  = "json"
        
        
        yield item
        '''
        item = MyprojectItem()
        item = collections.OrderedDict(item)
        item['bank_code']   = "spdb"#银行编码
        item['bank_name']   = "浦发银行"#银行名称
        item['bank_type']   = "1"#银行类型：
        item['prod_code']   = prod_code#产品编码
        item['prod_name']   = response.xpath('//table/tbody/tr[1]/td[2]/p/text()').extract()[0]
        zz = u'产品类型'
        #item['prod_type']   = response.xpath("//td[p[text()='%s']]/following-sibling::*/p/text()" %(zz)).extract()[0]#产品类型
        item['live_time']   = ""
        item['std_rate']    = ""
        zz = u'投资者认购金额'
        #item['start_amount'] = response.xpath("//td[p[text()='%s']]/following-sibling::*/p/text()" %(zz)).extract()[0]
        
        zz = [u'产品风险等级',u'风险评定']
        #risk_level = response.xpath("//td[p[text()='%s']] |//td[p[text()='%s']] " %(zz[0],zz[1]))
        #item['risk_level'] = risk_level.xpath('following-sibling::*/p/text()').extract()
        item['create_time'] = time.time()#抓取时间
        item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
        
        yield item
        \
        wealth_code = re.findall(r'C[1-9]\d*',body)[0]#wealth编码
        content = prod_code,wealth_code
        urls = "http://www.chinawealth.com.cn/lccpAllProJzyServlet.go"
        yield scrapy.FormRequest(
            urls,
            formdata = {'cpdjbm':wealth_code,'pagenum':'1','prod_code':prod_code},#1在售，0停止
            callback = self.get_data,
            dont_filter=True
        )
       
    def get_data(self,response):
        print response.request.body
        body=str(response.body)
        json_obj = json.loads(body)
        i = json_obj['List'][0]
        
        item = MyprojectItem()
        item = collections.OrderedDict(item)
        item['bank_code']   = "spdb"#银行编码
        item['bank_name']   = "浦发银行"#银行名称
        item['bank_type']   = "1"#银行类型：
        item['prod_code']   = ""#产品编码
        item['prod_name']   = i['cpms']
        item['prod_type']   = i['cpsylxms'].strip()#产品类型
        item['start_amount']= i['qdxsje']#起购金额
        item['live_time']   = i['qxms'].strip()#ProdLimit周期
        item['buying_start']= i['mjqsrq']
        item['buying_end']  = i['mjjsrq']
        item['std_rate']    = i['yjkhzdnsyl']#ProdProfit利率
        item['risk_level']  = i['fxdjms'].strip()#风险等级
        item['status']      = i['cpztms'].strip()
        item['create_time'] = time.time()#抓取时间
        item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
        item['wealth']      = i['cpdjbm']
        yield item
        '''