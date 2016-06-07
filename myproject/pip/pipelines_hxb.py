# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 华夏银行

import os,codecs,json,collections,time,re
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class HxbPipeline(object):

    def process_item(self, item, spider):
        
        
        #产品名字
        if len(item['prod_name']) > 0:
            item['prod_name'] = "".join(item['prod_name']).replace(" ","")

        #起购金额
        if len(item['start_amount']) > 0:
            item['start_amount'] = item['start_amount'][0]+"0000"
        #购买周期
        if len(item['buying_start']) == 1:
            item['buying_start'] = item['buying_start'][0]
            item['buying_end'] = item['buying_end'][0]
        else:
            item['buying_start'] = item['buying_start'][0]
            item['buying_end'] = item['buying_end'][2]
       
        item['buying_start'] = item['buying_start'].replace(".","-").replace(u"．","-")
        item['buying_end'] = item['buying_end'].replace(".","-").replace(u"．","-")
        item['buying_start'] = re.findall(r'\d*-\d*-\d*',item['buying_start'],re.M)
        item['buying_end'] = re.findall(r'\d*-\d*-\d*',item['buying_end'],re.M)
        if len(item['buying_start']) > 0:
            item['buying_start'] = item['buying_start'][0]
            item['buying_start'] = int(time.mktime(
                time.strptime(str(item['buying_start']), '%Y-%m-%d')
                ))
        else:
            item['buying_start'] = 0
            
        if len(item['buying_end']) > 0:
            item['buying_end'] = item['buying_end'][0]
            item['buying_end'] = int(time.mktime(
                time.strptime(str(item['buying_end']), '%Y-%m-%d')
                ))
        else:
            item['buying_end'] = 0
        #周期
        item['live_time'] = '0'
        
        #利率
        
        if len(item['std_rate']) > 0:
            item['std_rate'] = item['std_rate'][0].replace("%","").replace(" ","")
        else:
            item['std_rate'] = "0"
            
        #风险等级
        item['risk_level'] = "2"
        
        
        item['create_time'] = time.time()#抓取时间
        item['create_time2'] = time.strftime('%Y-%m-%d %H:%M:%S')#抓取时间
  
        return item