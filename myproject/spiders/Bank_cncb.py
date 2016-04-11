# -*- coding: utf-8 -*-
# 中信银行
# 遍历每个产品
import scrapy,json,codecs,time,os,re,collections
from myproject.items import MyprojectItem

class CnbcSpider(scrapy.spiders.Spider):
    name = "bank_cncb"
    allowed_domains = ["mall.bank.ecitic.com"]
    #抓取页面地址
    
    start_urls=['https://mall.bank.ecitic.com/fmall/pd/fin-index.htm']
    
    def __init__(self):
        #初始页与条数
        self.page=1
        self.row=1
    
    def parse(self, response):
        urls = "https://mall.bank.ecitic.com/fmall/pd/fin-index.htm"
        print "================START_REQUESTS============"
        #进行POST请求，提交相关参数
        yield scrapy.FormRequest(
            urls,
            formdata = {'currentpage':'%d' %self.page},
            callback = self.post_cnbc,
            dont_filter=True
        )
    
    def post_cnbc(self,response):
        #获取总页码
        text = str(response.body)
        test = re.findall(r'\'.eval\(\'(.*?)\'\)',text,re.M)
        totalPage = int(test[0])
        
       
        #提取区域
        sites = response.xpath('//table[@id="charttab"]//tr[@class="bg_hui"]')
        #print sites
        for i in sites:
            item = MyprojectItem()
            item = collections.OrderedDict(item)
            item['bank_code']   = "CNBC"#银行编码
            item['bank_name']   = "中信银行"#银行名称
            item['bank_type']   = "1"#银行类型：
            item['prod_code']   = i.xpath('td[2]//a/text()').extract()#产品编码
            item['prod_name']   = i.xpath('td[3]//a/text()').extract()#产品名称
            item['prod_type']   = "1"#产品类型
            
            start_amount = i.xpath('td[@param_type="first_amt"]//span/text()').extract()[0]#起购金额
            item['start_amount']= start_amount.replace(',','') + '0000'
            
            item['live_time']   = i.xpath('td[7]//span/text()').extract()#ProdLimit周期
            item['std_rate']    = i.xpath('td[8]//span/text()').extract()#ProdProfit利率
            item['risk_level']  = i.xpath('td[@param_type="risk_level"]//span/text()').extract()#风险等级
            
            item['create_time'] = time.time()#抓取时间
            item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
            item['total_data']  = ""#全部数据
            
            yield item
        try:
            if self.page < totalPage:
                self.page +=1
                
                print "正在读取...."
                print self.page
                urls = "https://mall.bank.ecitic.com/fmall/pd/fin-index.htm"
                yield scrapy.Request(urls, callback=self.parse,dont_filter=True)
        except:
            print "This Error"