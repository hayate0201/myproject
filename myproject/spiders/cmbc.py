# -*- coding: utf-8 -*-
import scrapy
import time
import json
from myproject.items import MyprojectItem
import codecs
import pymongo
import collections
import os

class CmbcSpider(scrapy.spiders.Spider):

    name = "cmbc"
    allowed_domains = ["cmbc.com.cn"]
    page=1
    start_urls=['https://service.cmbc.com.cn/pai_ms/cft/queryTssPrdInScreenfoForJson.gsp?page=%s&rows=10' %page]

    def __init__(self):
        self.page=1


    def parse(self, response):
        response_body=str(response.body)
        result=response_body[9:(len(response_body)-2)]
        print result
        json_obj=json.loads(result)
        #print json_obj
        item = MyprojectItem()
        item= collections.OrderedDict(item)
        BASE_PATH = os.getcwd() #获取当前scrapy项目根目录
        filename = os.path.join(BASE_PATH,"myproject/data/cmbc.txt")
        #bankname = u"民生银行"
        #判断最新的抓取页数,以及当前页行记录循环次数
        if json_obj['page']<json_obj['pageCount']:
            rows=json_obj['rows']
            page=json_obj['page']+1
            urls='https://service.cmbc.com.cn/pai_ms/cft/queryTssPrdInScreenfoForJson.gsp?page=%s&rows=10' %page
        elif json_obj['page']==json_obj['pageCount']:
            #取余数做循环
            rows=json_obj['rowCount']%json_obj['rows']
        with codecs.open(filename, 'a', encoding='utf-8') as f:
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
                    #普通spride，必须这里就做数据的迭代，否则出错；值全部会变
                    #yield item
                    line = item['bank_name'] + item['prod_code'] + item['prod_name'] + item['start_amount'] + \
                           item['live_time'] + item['std_rate'] + item['risk_level'] + "\n"
                    f.write(line)
                f.close()


        #url='''http://www.cmbc.com.cn/cs/Satellite?c=Page&cid=1356495592289&pagename=cmbc%2FPage%2
        #FTP_PersonalProductdShopLayOut&rendermode=preview&Type=1&TypeId=1356495507846&productId=FSAC14168N'''
        '''
        try:
            if 'urls' in dir():
                yield scrapy.Request(urls, callback=self.parse)
        except:

            print "this is error "
        '''

    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

    #获取当前时间
    def getCurrentDate(self):
        return time.strftime('%Y-%m-%d',time.localtime(time.time()))
    #写入日志
    #f_handler=open('out.log', 'w')
    #sys.stdout=f_handler/.,m