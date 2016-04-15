# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os,codecs,json,collections,time

class Pipelines(object):
    
    #写入item到json文件
    def process_item(self, item, spider):
        item['create_time'] = time.time()#抓取时间
        item['create_time2'] = time.strftime('%Y-%m-%d %H:%M:%S')#抓取时间
            
        line = json.dumps(collections.OrderedDict(item)) + "\n"
        self.file.write(line.decode("unicode_escape")) 
        return item
    
    #爬虫开始时创建对应文件
    def open_spider(self, spider):
        BASE_PATH = os.getcwd()
        dirname = os.path.join(BASE_PATH,"data")
        if not os.path.exists(dirname):
			os.makedirs(dirname)
        self.dir = os.path.join(dirname,spider.name+".json")
        self.file = codecs.open(self.dir, 'wb+', encoding='utf-8')
        self.file.write("")#清空文件内容