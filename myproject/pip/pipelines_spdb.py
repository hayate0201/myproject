# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 浦发银行

import os,codecs,json,collections,time,re
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class SpdbPipeline(object):

    def process_item(self, item, spider):
        #起购金额
        item['start_amount'] = int(float(item['start_amount'].replace(",","")))
        
        #购买周期
        try:
            item['buying_start'] = int(time.mktime(
                    time.strptime(item['buying_start'], '%Y/%m/%d')
                    ))
        except:
            item['buying_start'] = 0
            
        try:
            item['buying_end'] = int(time.mktime(
                    time.strptime(item['buying_end'], '%Y/%m/%d')
                    ))
        except:
            item['buying_end'] = 0
            
        #周期
        live_time = item['live_time'].replace(u"天","").replace("-","")
        item['live_time'] = live_time if live_time else "0"
        
        #利率
        std_rate = re.findall(r'(\d*\.\d*)%',item['std_rate'],re.M)
        item['std_rate'] = std_rate[0] if std_rate else "0"  
        return item