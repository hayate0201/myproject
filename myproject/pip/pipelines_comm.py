# -*- coding: utf-8 -*-
#交通银行

import os,codecs,json,collections,time,re
from scrapy.conf import settings

class CommPipeline(object):
    def process_item(self, item, spider):
        #起购金额
        item['start_amount'] = re.findall(ur'(\d*)万',item['start_amount'],re.M)
        if len(item['start_amount']) == 2:
            item['start_amount'] = item['start_amount'][1]+"0000"
        elif len(item['start_amount']) == 1:
            item['start_amount'] = item['start_amount'][0]+"0000"
        else:
            item['start_amount'] = "0"
        #购买周期
        
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
        
        #利率周期
        
        item['live_time'] = re.findall(r'(\d*)',item['live_time'],re.M)
        item['live_time'] = "".join(item['live_time'])
        if not item['live_time']:
            item['live_time'] = "0"
      
        #利率
        item['std_rate'] = item['std_rate'].replace("%","").split("~")
        
        if len(item['std_rate']) == 2:
            item['std_rate'] = item['std_rate'][1]
        elif len(item['std_rate']) == 1:
            item['std_rate'] = item['std_rate'][0]
        else:
            item['std_rate'] = 0
        if item['std_rate'] == "":
            item['std_rate'] = 0
        
        #风险等级
        item['risk_level'] = re.findall(r'(\d)',item['risk_level'],re.M)[0]  
        
        return item
