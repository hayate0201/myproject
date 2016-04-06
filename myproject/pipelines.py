# -*- coding: utf-8 -*-
import json
import codecs
import pymongo
import collections
import os
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MyprojectPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool
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
    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)
        
    #pipeline默认调用
    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._do_upinsert, item, spider)	
        d.addErrback(self._handle_error, item, spider)
        d.addBoth(lambda _: item)
        return d
    
    #将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
        #查找是否存在相同编码
        conn.execute('select 1 from bank_'+item['bank_code']+' where prod_code = %s', (item['prod_code']))
        ret = conn.fetchone()
        if ret:
            #更新
            conn.execute('update bank_'+item['bank_code']+' set prod_name="test",bank_name=%s where prod_code = %s',(item['bank_name'],item['prod_code']))
        else:
            #插入
            conn.execute('insert into bank_'+item['bank_code']+' values(null,%s,%s,%s)',(item['bank_name'],item['prod_code'],item['prod_name']))
    def spider_closed(self, spider):
        self.file.close()
        self.client.close()
        

