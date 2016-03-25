# -*- coding: utf-8 -*-
import scrapy
import time
import json
from myproject.items import MyprojectItem
import codecs
import os
import re
from bs4 import  BeautifulSoup

class HxbSpider(scrapy.spiders.Spider):

    name = "hxb"
    allowed_domains = ["hxb.com.cn"]
    start_urls=['http://www.hxb.com.cn/home/cn/personal/longying/licai/list.shtml']

    def parse(self, response):
        #response_body=str(response.body)
        html_doc=unicode(response.body, "utf-8")
        #print result
        BASE_PATH = os.getcwd() #获取当前scrapy项目根目录
        filename = os.path.join(BASE_PATH,"myproject/data/hxb.txt")
        #filename = "/Users/apple/PycharmProjects/scrapy-yinhang/myproject/myproject/data/hxb.txt"
        #pattern = re.compile(r'(?=pro_contp.*>).*?</div>',re.S)
        pattern = re.compile(r'<div class="pro_contp".*?<div class="pro_notice".*?</div>',re.S)
        result = pattern.findall(html_doc)
        #result = pattern.match(html_doc)
        #print result
        html_doc=""
        with codecs.open(filename, 'w', encoding='utf-8') as f:
            #f.write(result)
            for i in result:
                f.write(i)
                #html_doc=html_doc+i
            '''
                for i in range(0,rows):
                    item['bank_code']="cmbc"
                    #item['bank_name']="民生银行"
                    item['bank_name']=u"民生银行"
                    item['bank_type']="1"
                    item['prod_code']=json_obj['list'][i]['prd_code']
                    item['prod_name']=json_obj['list'][i]['prd_name']
                    item['prod_type']="1"
                    item['start_amount']=json_obj['list'][i]['pfirst_amt']
                    item['live_time']=json_obj['list'][i]['live_time']
                    item['std_rate']=json_obj['list'][i]['next_income_rate']
                    item['risk_level']=json_obj['list'][i]['risk_level']
                    item['create_time']=time.time()
                    item['total_type']="json"
                    item['total_data']=json_obj['list'][i]
                    '''
                    #普通spride，必须这里就做数据的迭代，否则出错；值全部会变
            #yield item

        soup = BeautifulSoup(html_doc)
        #print soup.title
        #print soup.title.name
        #print soup.title.string
        print soup.strong
        #print soup.a
        print soup.find_all('strong')
        #print soup.find(id='link3')
        #print soup.get_text()