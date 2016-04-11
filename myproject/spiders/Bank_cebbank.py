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
            callback = self.post_ecbb,
            dont_filter=True
        )
    
    def post_ecbb(self,response):
        #产品总数目
        sel = scrapy.Selector(response)
        total = sel.xpath('//*[@id="pagingDiv"]/table/tbody/tr/td[2]/i/text()').extract()[0] 
        total = int(total,10) #转为整数方便做比较
        #print total
        #提取区域
        sites = response.xpath('//table[@class="zslccp"]/tbody/tr[@align]')
        for site in sites:
            item = MyprojectItem()
            item = collections.OrderedDict(item)
            item['bank_code']   = "ecbb"#银行编码
            item['bank_name']   = "光大银行"#银行名称
            item['bank_type']   = "1"#银行类型：
            item['prod_code']   = site.xpath('normalize-space(td[1]/text())').extract()#产品编码
            item['prod_name']   = site.xpath('normalize-space(td[2]/a/text())').extract()#产品名称
            item['prod_type']   = "1"#产品类型
            item['start_amount']= site.xpath('normalize-space(td[7]/text())').extract()#起购金额
            item['live_time']   = "unknow"#ProdLimit周期
            item['std_rate']    = site.xpath('normalize-space(td[9]/text())').extract()#ProdProfit利率
            item['risk_level']  = site.xpath('normalize-space(td[10]/text())').extract()#风险等级
            item['create_time'] = time.time()#抓取时间
            item['total_type']  = "json"#全部数据类型：XML,JSON,HTML,ARRAY
            item['total_data']  = ""#全部数据
            
            self.row +=1
            yield item
        try:
            if self.row < total:
                #如果当前总收录小于总数，回调parse    
                self.page+=1
                urls = "http://www.cebbank.com/eportal/ui?pageId=478550&currentPage=%s&moduleId=12218" %self.page
                print "GO NEXT PAGE...."
                yield scrapy.Request(urls,callback=self.parse,dont_filter=True)
        except:
            print "This Error"