# -*- coding: utf-8 -*-
#中信银行

import os,codecs,json,collections,time,re
from scrapy.conf import settings

class CncbPipeline(object):
    def process_item(self, item, spider):
        #购买周期
        item['buying_start'] = re.findall(r'\d*-\d*-\d*',item['buying_start'],re.M)
        item['buying_end'] = re.findall(r'\d*-\d*-\d*',item['buying_end'],re.M)
        
        
        if len(item['buying_end']) > 0:
            item['buying_end'] = item['buying_end'][0]
            item['buying_end'] = int(time.mktime(
                time.strptime(str(item['buying_end']), '%Y-%m-%d')
                ))
        else:
            item['buying_end'] = 0
        if item['buying_end'] == 0:
            item['buying_start'] = 0
        else:
            if len(item['buying_start']) > 0:
                item['buying_start'] = item['buying_start'][0]
                item['buying_start'] = int(time.mktime(
                    time.strptime(str(item['buying_start']), '%Y-%m-%d')
                    ))
            else:
                item['buying_start']
        
        #利率周期
        item['live_time'] = re.findall(r'(\d*)',item['live_time'],re.M)
        item['live_time'] = "".join(item['live_time'])
        if not item['live_time']:
            item['live_time'] = "0"
            
        #利率
        item['std_rate'] = item['std_rate'].replace("%","")
        
        #风险等级
        item['risk_level'] = item['risk_level'].replace(u"较低风险","2").replace(u"较高风险","4")\
                            .replace(u"中等风险","3").replace(u"低风险","1").replace(u"高风险","5")
                       
            
        return item
