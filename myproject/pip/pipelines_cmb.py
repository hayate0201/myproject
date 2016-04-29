# -*- coding: utf-8 -*-
#招商

import os,codecs,json,collections,time,re
from scrapy.conf import settings

class CmbPipeline(object):
    def process_item(self, item, spider):
        #起购金额
        item['start_amount'] = item['start_amount'].replace(",","")
        
        #周期
        item['live_time'] = re.findall(r'(\d*)',item['live_time'],re.M)[0]
        if not item['live_time']:
            item['live_time'] = 0
        
            
        #购买时间
        try:
            item['buying_start'] = time.mktime(
                    time.strptime(item['buying_start'], '%Y-%m-%d')
                    )
        except:
            item['buying_start'] = 0
            
        try:
            item['buying_end'] = time.mktime(
                    time.strptime(item['buying_end'], '%Y-%m-%d')
                    )
        except:
            item['buying_end'] = 0   
        
        #风险等级
        item['risk_level'] = re.findall(r'(\d)',item['risk_level'],re.M)[0]
        
        #利率
        item['std_rate'] = re.findall(r'([0-9\.])',item['std_rate'],re.M)
        item['std_rate'] = "".join(item['std_rate'])
        if not item['std_rate']:
            item['std_rate'] = '0'
        return item
