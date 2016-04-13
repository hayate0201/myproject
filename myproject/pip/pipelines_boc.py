# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#中国银行管道

import pymongo
from scrapy.conf import settings

class BocPipeline(object):

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
        

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #print spider.name
        #collection_name = "BOC"
        key = {'prod_code':item['prod_code']}
        self.db[spider.name].update(key,item,upsert=True)
        return item