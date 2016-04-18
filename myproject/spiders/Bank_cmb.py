# -*- coding: utf-8 -*-
#招商银行
#from scrapy.selector import Selector
import scrapy,json,codecs,time,os,re,collections
from myproject.items import MyprojectItem
class CmbSpider(scrapy.spiders.Spider):

    name = "bank_cmb"
    allowed_domains = ["cmbchina.com"]
    start_urls=[
        'http://www.cmbchina.com/cfweb/svrajax/product.ashx?op=search&type=m&pageindex=1&salestatus=A&baoben=&currency=&term=&keyword=&series=01&pagesize=20&orderby=ord1'
        ]
        
    #自定义管道
    custom_settings = {
        'ITEM_PIPELINES':{
            'myproject.pipelines.Pipelines': 100,
            'myproject.pip.pipelines_mongo.MongodbPipeline': 200
        }
    }
    def __init__(self):
        self.page=1
        self.row=1
        
    def parse(self, response):
        
        
        #切割字符串，选择字符串
        response_body=str(response.body)
        result=response_body[1:(len(response_body)-1)]
        
        #转为json格式,通过正则转换键名
        s1 = re.sub(r'(\w+:)', r'"\1:', result)
        s1 = re.sub(r'(::)', r'":', s1)
 
        json_obj=json.loads(s1)
        
        total = json_obj['totalPage'] #提取总页数
        print "GetData  Status Page:%d/%d" %(self.page,total)

        for i in json_obj['list']:
            code = i['PrdCode']#产品编码
            content = json.dumps(i)
            urls = 'http://www.cmbchina.com/cfweb/Personal/productdetail.aspx?code=%s&type=prodinfo' %code
            yield scrapy.Request(urls,callback=self.get_data,body=content,dont_filter=True)
            
        
        try:
            if self.page < total:
                self.page += 1
                urls = 'http://www.cmbchina.com/cfweb/svrajax/product.ashx?' + \
                    'op=search&type=m&pageindex=%d&salestatus=A&baoben=&currency=&term=&keyword=&series=01&pagesize=20&orderby=ord1' %self.page
                print "GO NEXT PAGE...."
                print urls
                yield scrapy.Request(urls,callback=self.parse,dont_filter=True)
                
        except:
            print "This Error"
        
        
    def get_data(self,response):
        i =json.loads(response.request.body)
        money = response.xpath('normalize-space(//table[@class="buyinfo"]//tr[3]/td[4]/text())').extract()[0]
        item = MyprojectItem()
        item = collections.OrderedDict(item)
        item['bank_code']   = "Cmb"#银行编码
        item['bank_name']   = "招商银行"#银行名称
        item['bank_type']   = "1"#银行类型：
        item['prod_code']   = i['PrdCode']#产品编码
        item['prod_name']   = i['PrdName']#产品名称
        item['prod_type']   = i['TypeCode']#产品类型
        item['start_amount']= money#起购金额
        item['live_time']   = i['FinDate']#ProdLimit周期
        item['buying_start']= i['BeginDate']
        item['buying_end']  = i['EndDate']
        item['std_rate']    = i['NetValue']#ProdProfit利率
        item['risk_level']  = i['Risk']#风险等级
        item['status']      = i['IsCanBuy']
        item['create_time'] = time.time()#抓取时间
        item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
            
        yield item
