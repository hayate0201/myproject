# -*- coding: utf-8 -*-
# 兴业银行银行

import scrapy,json,codecs,time,os
from myproject.items import MyprojectItem

class ccbSpider(scrapy.spiders.Spider):
    name = "cib"
    allowed_domains = ["http://directbank.cib.com.cn/"]
    #抓取页面地址
    Settime = time.time()
    start_urls=[
        'http://directbank.cib.com.cn/hall/show/fin/finlist!ajaxPage.do?dataSet.nd=%s&dataSet.rows=3000&dataSet.page=1' %Settime
        ]
    
    def __init__(self):

        #文件设置
        BASE_PATH = os.getcwd()
        self.dir = os.path.join(BASE_PATH,"myproject/data/cib.json")
        self.file = codecs.open(self.dir, 'wb+', encoding='utf-8')
        self.file.write("")#清空文件内容
    
    def parse(self, response):
        
        #保存文件路径
        self.file = codecs.open(self.dir, 'a+', encoding='utf-8')
        
        json_obj = json.loads(response.body_as_unicode())
        total = json_obj['total'] #当前提取总数

        for i in json_obj['rows']:
            item = MyprojectItem()
            item['bank_code']   = "cib"#银行编码
            item['bank_name']   = "兴业银行"#银行名称
            item['bank_type']   = "1"#银行类型
            item['prod_code']   = i['finCode']#产品编码
            item['prod_name']   = i['finName']#产品名称
            item['prod_type']   = ""#产品类型
            item['start_amount']= i['minAmt']#起购金额
            item['live_time']   = i['timeLimit']#ProdLimit周期
            item['std_rate']    = i['referenceIncome']#ProdProfit利率
            item['risk_level']  = i['prodRRName']#风险等级
            item['create_time'] = time.time()#抓取时间
            item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
            #item['total_data']  = i#全部数据
            line = json.dumps(dict(item)) + '\n'
            self.file.write(line.decode("unicode_escape")) 
            
        