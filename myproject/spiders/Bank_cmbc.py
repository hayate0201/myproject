# -*- coding: utf-8 -*-
import scrapy,json,codecs,time,os,re,collections
from myproject.items import MyprojectItem

class CmbcSpider(scrapy.spiders.Spider):

    name = "bank_cmbc"
    allowed_domains = ["cmbc.com.cn"]
    page=1
    start_urls=['https://service.cmbc.com.cn/pai_ms/cft/queryTssPrdInScreenfoForJson.gsp?page=%s&rows=10' %page]

    def __init__(self):
        self.page=1
        self.row=1


    def parse(self, response):
        response_body=str(response.body)
        result=response_body[9:(len(response_body)-2)]
        json_obj=json.loads(result)
        total = json_obj['pageCount'] #提取总页数
        print "GetData  Status Page:%d/%d" %(self.page,total)
        for i in json_obj['list']:
            code = i['prd_code']#产品编码
            urls = 'https://service.cmbc.com.cn/pai_ms/cft/queryForObject.gsp?&params.prd_code=%s&params.type=TSS' %code
            yield scrapy.Request(urls,callback=self.get_data,dont_filter=True)

        #https://service.cmbc.com.cn/pai_ms/cft/queryForObject.gsp?&params.prd_code=FSAA16151B&params.type=TSS
        try:
            if self.page < total:
                self.page += 1
                urls = 'https://service.cmbc.com.cn/pai_ms/cft/queryTssPrdInScreenfoForJson.gsp?page=%s&rows=10' %self.page
                print "GO NEXT PAGE...."
                print urls
                yield scrapy.Request(urls,callback=self.parse,dont_filter=True)
                
        except:
            print "This Error"
    def get_data(self,response):
        response_body=str(response.body)
        result=response_body[9:(len(response_body)-2)]
        i=json.loads(result)
        
        item = MyprojectItem()
        item = collections.OrderedDict(item)
        item['bank_code']   = "cmbc"#银行编码
        item['bank_name']   = "民生银行"#银行名称
        item['bank_type']   = "1"#银行类型：
        item['prod_code']   = i['prd_code']#产品编码
        item['prod_name']   = i['prd_name']#产品名称
        item['prod_type']   = i['prd_type_name'].strip()#产品类型
        item['start_amount']= i['pfirst_amt']#起购金额
        item['live_time']   = i['liv_time_unit_name'].strip()#ProdLimit周期
        item['buying_start']= i['ipo_start_date']
        item['buying_end']  = i['ipo_end_date']
        item['std_rate']    = i['next_income_rate']#ProdProfit利率
        item['risk_level']  = i['risk_level_name'].strip()#风险等级
        item['status']      = i['status_name'].strip()
        item['create_time'] = time.time()#抓取时间
        item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
        
        yield item
       