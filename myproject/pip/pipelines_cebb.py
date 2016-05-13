# -*- coding: utf-8 -*-
#光大

import os,codecs,json,collections,time,re
from scrapy.conf import settings

class CebbPipeline(object):
    def process_item(self, item, spider):
        #起购金额
        item['start_amount'] = int(float(item['start_amount'].replace(",","")))
        
        #周期
        item['live_time'] = item['live_time'].replace(u"1年","365").replace(u"日/期","")\
                            .replace(u"个月","-30").replace(u"一年","365").replace(u"日","")
        item['live_time'] = item['live_time'].split("-")
        if len(item['live_time']) > 1:
            item['live_time'] = str(int(item['live_time'][0])*int(item['live_time'][1]))
        else:
            item['live_time'] = item['live_time'][0]
            
        #购买时间
        item['buying_start'] = item['buying_start'].replace("-","")
        item['buying_end'] = item['buying_end'].replace("-","")
        if item['buying_start']:
            item['buying_start'] = int(time.mktime(
                time.strptime(str(item['buying_start']), '%Y%m%d')
                ))
            item['buying_end'] = int(time.mktime(
                time.strptime(str(item['buying_end']), '%Y%m%d')
                )) 
        else:
            item['buying_start'] = 0
            item['buying_end'] = 0
            
        #风险等级
        item['risk_level'] = item['risk_level'].replace(u"较低","2").replace(u"较高","4")\
                            .replace(u"中","3").replace(u"低","1").replace(u"高","5")
        #利率
        item['std_rate'] = item['std_rate'].replace("%","")
        item['std_rate'] = item['std_rate'].split("-")
        if len(item['std_rate']) == 2:
            item['std_rate'] = item['std_rate'][1]
        elif len(item['std_rate']) == 1:
            item['std_rate'] = item['std_rate'][0]
        else:
            item['std_rate'] = 0
        if item['std_rate'] == "":
            item['std_rate'] = 0
        return item
