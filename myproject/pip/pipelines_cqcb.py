# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 重庆银行

import os,codecs,json,collections,time,re
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class CqcbPipeline(object):

    def process_item(self, item, spider):
        if item['prod_name'] and item['buying_start'] and item['live_time'] and item['std_rate']\
            and item['risk_level'] and item['prod_name'] != u"产品名称":
            #购买周期
            buyingTime = item['buying_start']
            if len(buyingTime) == 1:
                item['buying_start'] = 0
                item['buying_end'] = 0
            else:
                item['buying_start'] = int(time.mktime(
                time.strptime(str(buyingTime[0]), '%Y.%m.%d')
                ))
                item['buying_end'] = int(time.mktime(
                time.strptime(str(buyingTime[1]), '%Y.%m.%d')
                ))
            #周期
            live_time = item['live_time'].replace(u"天","")
            item['live_time'] = live_time if live_time.isdigit() else "0"
            #利率
            item['std_rate'] = item['std_rate'].replace("%","").replace(" ","")
            #风险等级
            item['risk_level'] = item['risk_level'].replace(u"中低风险","2").replace(u"中高风险","4")\
                            .replace(u"低风险","1").replace(u"中风险","3").replace(u"高风险","5")
            #item['prod_name'] = item['prod_name'].encode("utf-8","ignore")          
            return item
        else:
            raise DropItem(u"丢弃") 