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
        item['start_amount'] = item['start_amount'][0].replace(u"万","0000")
        item['start_amount'] = " ".join(re.findall(r'(\d*)', item['start_amount'], re.M|re.I)).split()
        if len(item['start_amount']) >0:
            item['start_amount'] = item['start_amount'][0]
        else:
            item['start_amount'] = "0"
        
        
        #购买周期
        try:
            item['buying_start'] = int(time.mktime(
                    time.strptime("20"+str(item['buying_start']), '%Y%m%d')
                    ))
        except:
            item['buying_start'] = 0
            
        try:
            item['buying_end'] = int(time.mktime(
                    time.strptime("20"+str(item['buying_end']), '%Y%m%d')
                    ))
        except:
            item['buying_end'] = 0
        
        #周期
        item['live_time'] = item['live_time'].replace(u"天","").replace(u"月","x30").replace(u"季","30")
        item['live_time'] = "".join(re.findall(r'([0-9x]*)', item['live_time'], re.M|re.I))
        item['live_time'] = item['live_time'].split("x")
        if not item['live_time'][0]:
            item['live_time'] = 0
        elif len(item['live_time']) >1:
            item['live_time'] = str(int(item['live_time'][0])*int(item['live_time'][1]))
        else:
            item['live_time'] = item['live_time'][0]
        
        #利率
        item['std_rate'] = re.findall(r'(\d*\.\d*)%',item['std_rate'],re.M)
        if len(item['std_rate']) > 0:
            item['std_rate'] = item['std_rate'][0]
        else:
            item['std_rate'] = "0"
            
       
        #风险等级
        if not item['risk_level']:
            item['risk_level'] = 0
        else:
            item['risk_level'] = item['risk_level'][0].replace(u"较低","2").replace(u"较高","4") \
                        .replace(u"低","1").replace(u"中","3").replace(u"高","5")
            item['risk_level'] = re.findall(r'\d',item['risk_level'],re.M)[0]
              
        return item