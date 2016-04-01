# -*- coding: utf-8 -*-
import json
import codecs
import pymongo
import collections
import os
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MyprojectPipeline(object):

    def __init__(self):
        print "__INIT__"
        '''
        #self.file = codecs.open('hxb.txt', 'a', encoding='utf-8')
        BASE_PATH = os.getcwd() #获取当前scrapy项目根目录
        filename = os.path.join(BASE_PATH,"myproject/data/cmbc.json")
        self.file = codecs.open(filename, 'a', encoding='utf-8')
        #self.mongo_host = "localhost"
        #self.mongo_port="27017"
        #self.mongo_db = "local"
        self.client = pymongo.MongoClient("localhost",27017)
        self.db = self.client.local
        self.col=self.db.test2
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )
        '''
    def process_item(self, item, spider):
        print "process_item"
        print item['bank_code']
        '''
        print type(item['risk_level'])
        #这里可以加判断,这里特别注意：显示转换后比较才生效，否则以unicode编码格式比较

        if int(item['risk_level'])<3:
            line = json.dumps(collections.OrderedDict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
            #self.file.write(dict(item))
        #写入mongodb
        self.col.save(collections.OrderedDict(item))
        return item
        
        print "------------"
        print item
        print "------------"
        line = item['prod_code'] + item['prod_name'] + item['start_amount'] +
               item['live_time'] + item['std_rate'] + item['risk_level'] + "n"
        self.file.write(line)
        return item
        '''



    def spider_closed(self, spider):
        self.file.close()
        self.client.close()


