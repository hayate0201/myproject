# -*- coding: utf-8 -*-
import scrapy,json,codecs,time,os,collections,re
from myproject.items import MyprojectItem

class HxbSpider(scrapy.spiders.Spider):

    name = "bank_hxb"
    allowed_domains = ["hxb.com.cn"]
    start_urls=['http://www.hxb.com.cn/home/cn/personal/longying/licai/list.shtml']
    
    #自定义管道
    custom_settings = {
        'ITEM_PIPELINES':{
            'myproject.pip.pipelines_hxb.HxbPipeline': 1,
            'myproject.pipelines.Pipelines': 100,
            'myproject.pip.pipelines_mongo.MongodbPipeline': 200
        }
    }
    
    def __init__(self):
        self.row_time = 0
        self.row_name = 0
        self.row_type = 0
        self.last_name = ""
        self.last_type = ""
        self.last_time = ""
    def parse(self, response):
        sites = response.xpath('//table/tbody/tr')
        
        for i in sites:
            item = MyprojectItem()
            item = collections.OrderedDict(item)
            #单个产品
            item['bank_code']   = "hxb"#银行编码
            item['bank_name']   = "华夏银行"#银行名称
            
            item['bank_type']   = "1"#银行类型
            item['prod_code']   = ""#产品编码
            item['prod_name']   = "".join(i.xpath('td[1]/p/text()').extract())#产品名称
            #print item['prod_name']
            
            item['buying_start']= i.xpath('td[2]/p/text()').extract()
            item['buying_end']  = i.xpath('td[2]/p/text()').extract()
            
            item['prod_type']   = ""
            item['start_amount']= i.xpath('td[4]/p/text()').extract()
            item['coin_type']   = "人民币"
            item['live_time']   = ""#ProdLimit周期
            item['std_rate']    = i.xpath('td[3]/p/text()').extract()#ProdProfit利率
            item['risk_level']  = ""#风险等级
            
            #解析产品表单
            row_name = i.xpath('td[1]/@rowspan').extract()
            row_time = i.xpath('td[2]/@rowspan').extract()
            row_type = i.xpath('td[6]/@rowspan').extract()
            
            #是否是第一个系列产品
            if row_name: 
                self.row_name = int(row_name[0])
                self.last_name = item['prod_name']
                #时间线是否是第一个
                if row_time:
                    self.row_time = int(row_time[0])
                    self.last_time = i.xpath('td[2]/p/text()').extract()
                    item['buying_start'] = self.last_time
                    item['buying_end'] = self.last_time
                    item['start_amount'] = i.xpath('td[4]/p/text()').extract()
                    item['std_rate'] = i.xpath('td[3]/p/text()').extract()
                    item['prod_name']= self.last_name+"-"+str(item['start_amount'][0])+u"万"
                elif self.row_time >1:
                    self.row_time -=1
                    item['start_amount'] = i.xpath('td[3]/p/text()').extract()
                    item['std_rate'] = i.xpath('td[2]/p/text()').extract()
                    item['buying_start'] = self.last_time
                    item['buying_end'] = self.last_time
                    item['prod_name']= self.last_name+"-"+str(item['start_amount'][0])+u"万"
            elif self.row_name > 1:#子产品
                self.row_name -=1
                item['start_amount'] = i.xpath('td[2]/p/text()').extract()
                item['std_rate'] = i.xpath('td[1]/p/text()').extract()
                item['buying_start'] = self.last_time
                item['buying_end'] = self.last_time
                item['prod_name']= self.last_name+"-"+str("".join(item['start_amount']))+u"万"
                
            if row_type:
                self.last_type = i.xpath('td[6]/p/text()').extract()[0]
                item['prod_type'] = self.last_type
            else:
                item['prod_type'] = self.last_type
                
                
            #print item['prod_name']
            yield item

            