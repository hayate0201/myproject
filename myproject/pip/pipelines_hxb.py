# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#中国银行管道

import os,codecs,json,collections,time
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class hxbPipeline(object):

    def process_item(self, item, spider):
        if len(item['prod_name']) > 0:
            item['prod_name'] = "".join(item['prod_name'])
            if len(item['buying_start']) == 1:
                item['buying_start'] = item['buying_start'][0]
                item['buying_end'] = item['buying_end'][0]
            else:
                item['buying_start'] = item['buying_start'][0]
                item['buying_end'] = item['buying_end'][2]
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