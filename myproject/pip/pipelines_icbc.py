# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#工商银行

import os,codecs,json,collections,time,re
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class IcbcPipeline(object):

    def process_item(self, item, spider):
        print item['prod_name']
        #起购金额
        item['start_amount'] = item['start_amount'].replace(".00","").replace("-","0")
        
        #货币类型
        item['coin_type']   = "人民币"
        #购买周期
        try:
            item['buying_start'] = int(time.mktime(
                    time.strptime(str(item['buying_start']), '%Y%m%d')
                    ))
        except:
            item['buying_start'] = 0
        try:
            item['buying_end'] = int(time.mktime(
                    time.strptime(str(item['buying_end']), '%Y%m%d')
                    ))
        except:
            item['buying_end'] = 0
        
        #周期
        item['live_time'] = "".join(re.findall(r'(\d*)',item['live_time'],re.M))
        if not item['live_time']:
            item['live_time'] = "0"
        
        #利率
        
        item['std_rate'] = re.findall(r'(\d*\.\d*)%',item['std_rate'],re.M)
        
        if len(item['std_rate']) == 2:
            item['std_rate'] = item['std_rate'][1]
        elif len(item['std_rate']) == 1:
            item['std_rate'] = item['std_rate'][0]
        else:
            item['std_rate'] = "0"
            
        item['std_rate'] = round(float(item['std_rate']), 2)
        
        #风险等级
        #item['risk_level'] = "0"
        
        return item