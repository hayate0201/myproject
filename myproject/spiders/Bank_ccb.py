# -*- coding: utf-8 -*-
# 建设银行
# 需要通过POST请求抓取数据
# 遍历每个产品
import scrapy,json,codecs,time,os,collections
from myproject.items import MyprojectItem

class ccbSpider(scrapy.spiders.Spider):
    name = "bank_ccb"
    allowed_domains = ["ccb.com"]
    #抓取页面地址
    
    start_urls=[
        'http://finance.ccb.com/cc_webtran/queryFinanceProdList.gsp'
        ]
    
    def __init__(self):
        #初始页与条数，理财系列类型
        self.page=1
        self.row=0
        self.type=1
        
    def parse(self, response):
        urls = "http://finance.ccb.com/cc_webtran/queryFinanceProdList.gsp"
        print "================START_REQUESTS============"
        #进行POST请求，提交相关参数
        yield scrapy.FormRequest(
            urls,
            formdata = {
                'pageNo':'%d' %self.page,
                'pageSize':'15',
                #'queryForm.allOrgFlag':'1',
                'queryForm.brand':'0%d' %self.type, #03乾元 01利得盈 02建行财富 04汇得盈 05其它
                'queryForm.saleStatus':'-1',#销售状态
                }, 
            callback = self.post_ccb,
            dont_filter=True
        )
    
    def post_ccb(self,response):
        json_obj = json.loads(response.body_as_unicode()) 
        total = json_obj['totalCount'] #当前提取总数
        print "Total:%d" %total
        print "NOW Status TYPE:%d Page:%d" %(self.type,self.page)
        #print json_obj['ProdList']
        #开始提取
        for i in json_obj['ProdList']:
            item = MyprojectItem()
            item = collections.OrderedDict(item)
            item['bank_code']   = "ccb"#银行编码
            item['bank_name']   = "建设银行"#银行名称
            item['bank_type']   = "1"#银行类型
            item['prod_code']   = i['code']#产品编码
            item['prod_name']   = i['name']#产品名称
            item['prod_type']   = self.type#产品类型
            item['start_amount']= i['purFloorAmt']#起购金额
            item['live_time']   = i['investPeriod']#ProdLimit周期
            item['std_rate']    = i['yieldRate']#ProdProfit利率
            item['risk_level']  = i['riskLevel']#风险等级
            item['create_time'] = time.time()#抓取时间
            item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
            #item['total_data']  = i#全部数据

            self.row +=1
            yield item
        
        urls = "http://finance.ccb.com/cc_webtran/queryFinanceProdList.gsp"
        try:
            if self.row < total:
                #如果当前总收录小于总数，回调parse    
                self.page+=1
                print "GO NEXT PAGE...."
                yield scrapy.Request(urls,callback=self.parse,dont_filter=True)
            elif self.type < 5:
                self.type +=1
                print "GOTO NEXT TYPE: 0%d" %self.type
                self.page = 1
                self.row  = 0
                yield scrapy.Request(urls,callback=self.parse,dont_filter=True)
        except:
            print "This Error"
        
        