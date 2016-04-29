# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#把数据导入到mongodb

import pymongo,datetime,os,codecs,time
from scrapy.conf import settings

class MongodbPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('mongodb://localhost:27017'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'test')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        print "Create Mongodb.txt"
        BASE_PATH = os.getcwd()
        self.dir = os.path.join(BASE_PATH,"mongodbError.txt")
        self.file = codecs.open(self.dir, 'a+', encoding='utf-8')
        
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        today = datetime.date.today()
        time_line = datetime.datetime.strftime(today, '%Y%m%d')
        item['time_line'] = time_line
        key = {
            'prod_name':item['prod_name'],
            'prod_code':item['prod_code'],
            'time_line':item['time_line'],
            }
        collname = "bank"
        try:
            self.db[collname].update(key,item,upsert=True)
        except:
            nowtime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
            errorinfo = u"Error Code: %s 时间：%s\r\n" %(item['prod_code'],nowtime)
            self.file.write(errorinfo) 
        return item