# -*- coding: utf-8 -*-
# 光大银行
# 遍历每个产品
import scrapy,json,codecs,time,os,collections
from myproject.items import MyprojectItem

class cebbSpider(scrapy.spiders.Spider):
    name = "bank_cebb"
    allowed_domains = ["www.cebbank.com/"]
    #抓取页面地址
    
    start_urls=[
        'http://www.cebbank.com/eportal/ui?pageId=478550&currentPage=1&moduleId=12218'
        ]
    
    #自定义管道
    custom_settings = {
        'ITEM_PIPELINES':{
            'myproject.pip.pipelines_cebb.CebbPipeline': 1,
            'myproject.pipelines.Pipelines': 100,
            'myproject.pip.pipelines_mongo.MongodbPipeline': 200
        }
    }
    
    def __init__(self):
        #初始页与条数
        self.page=1
        self.row=1
        
        #文件设置
        BASE_PATH = os.getcwd()
        dirname = os.path.join(BASE_PATH,"data")
        if not os.path.exists(dirname):
			os.makedirs(dirname)
        self.dir = os.path.join(dirname,self.name+".json")
        self.file = codecs.open(self.dir, 'wb+', encoding='utf-8')
        self.file.write("")#清空文件内容
    
    def parse(self, response):
        
        urls = "http://www.cebbank.com/eportal/ui?pageId=478550&currentPage=%d&moduleId=12218" %self.page
        print "================START_REQUESTS============"
        #进行POST请求，提交相关参数
        yield scrapy.FormRequest(
            urls,
            formdata = {'filter_combinedQuery_SFZS':'1'},#1在售，0停止
            callback = self.get_url,
            dont_filter=True
        )
        '''
        urls = 'http://www.cebbank.com/site/gryw/yglc/lccpsj/Tjh70/16445370/index.html'
        yield scrapy.Request(urls,callback=self.get_data,dont_filter=True)
        '''
    def get_url(self,response):
        #产品总数目
        sel = scrapy.Selector(response)
        total = sel.xpath('//*[@id="pagingDiv"]/table/tbody/tr/td[2]/i/text()').extract()[0] 
        total = int(total) #转为整数方便做比较
        #print total
        
        sites = response.xpath('//table[@class="zslccp"]/tbody/tr[@align]')
        for i in sites:
            url = i.xpath('td[2]/a/@href').extract()[0]#
            obj = {}
            obj['std_rate'] = i.xpath('normalize-space(td[9]/text())').extract()[0]
            obj['prod_type']= i.xpath('normalize-space(td[5]/text())').extract()[0]
            content = str(obj)
            urls = "http://www.cebbank.com%s" %url
            yield scrapy.Request(urls,callback=self.get_data,body=content,dont_filter=True)
            self.row +=1
        
        try:
            if self.row < total:
                #如果当前总收录小于总数，回调parse    
                self.page+=1
                urls = "http://www.cebbank.com/eportal/ui?pageId=478550&currentPage=%s&moduleId=12218" %self.page
                print "GO NEXT PAGE...."
                yield scrapy.Request(urls,callback=self.parse,dont_filter=True)
        except:
            print "This Error"
        
    def get_data(self,response):
        obj = eval(response.request.body)
        #提取区域
        site = response

        item = MyprojectItem()
        item = collections.OrderedDict(item)
        item['bank_code']   = "cebb"#银行编码
        item['bank_name']   = "光大银行"#银行名称
        item['bank_type']   = "1"#银行类型：
        item['prod_code']   = response.xpath('//*[@id="cpbh"]/text()').extract()[0]#产品编码
        item['prod_name']   = response.xpath('//table/tbody/tr[1]/td/b/text()').extract()[0]#产品名称
        item['prod_type']   = obj['prod_type']#产品类型
        item['start_amount']= response.xpath('normalize-space(//*[@id="qgje"]/text())').extract()[0]#起购金额
        item['coin_type']   = response.xpath('normalize-space(//*[@id="tzbz"]/text())').extract()[0]#起购金额
        item['live_time']   = response.xpath('normalize-space(//*[@id="cpqx"]/text())').extract()[0]#周期
        item['buying_start']= response.xpath('normalize-space(//*[@id="xsqsr"]/text())').extract()[0]#起始日期
        item['buying_end']  = response.xpath('normalize-space(//*[@id="xszzr"]/text())').extract()[0]#结束日期
        item['std_rate']    = obj['std_rate']#ProdProfit利率
        item['risk_level']  = response.xpath('normalize-space(//*[@id="fxdj"]/text())').extract()[0]#风险等级
        item['status']      = response.xpath('normalize-space(//*[@id="cpzt"]/text())').extract()[0]#产品状态
        item['create_time'] = time.time()#抓取时间
        item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
   
        yield item
            