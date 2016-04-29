# -*- coding: utf-8 -*-
#民生

import os,codecs,json,collections,time,re
from scrapy.conf import settings

class CmbcPipeline(object):
    def process_item(self, item, spider):
        #起购金额
        item['start_amount'] = int(float(item['start_amount'].replace(",","")))
        
        #购买时间
        try:
            item['buying_start'] = time.mktime(
                time.strptime(item['buying_start'], '%Y-%m-%d'))
        except:
            item['buying_start'] = 0
        try:
            item['buying_end'] = time.mktime(
                time.strptime(item['buying_end'], '%Y-%m-%d'))
        except:
            item['buying_end'] = 0  

        #周期
        item['live_time'] = item['live_time'].replace(u"天","").replace(u"月","-30").split("-")
        if len(item['live_time']) ==1:
            item['live_time'] = int(item['live_time'][0])
        else:
            item['live_time'] = int(item['live_time'][0])*int(item['live_time'][1])
        
        #风险等级
        item['risk_level'] = item['risk_level'].replace(u"一","1").replace(u"二","2") \
                        .replace(u"三","3").replace(u"四","4").replace(u"五","5")
        item['risk_level'] = re.findall(r'(\d)',item['risk_level'],re.M)[0]
        
        #利率
        item['std_rate'] = item['std_rate'].replace("%","")
            
        return item
