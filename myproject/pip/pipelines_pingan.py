# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 平安银行

import os,codecs,json,collections,time,re
from scrapy.conf import settings
from scrapy.exceptions import DropItem

class PinganPipeline(object):

    def process_item(self, item, spider):
        #起购金额
        item['start_amount'] = item['start_amount'][0].replace(u" ","").replace(" ","") \
                .replace(u"万元","0000").replace(u"万港元","0000").replace(u"美元","")\
                .replace(",","")
        if not item['start_amount']:
            item['start_amount'] = 0
            
        #币种
        if len(item['coin_type']) >0:
            item['coin_type'] = item['coin_type'][0]
        else:
            item['coin_type'] = "人民币"
        #类型
        
        #购买周期
        item['buying_start'] = "".join(re.findall(r'(\d*)',item['buying_start'][0],re.M))
        item['buying_end'] = "".join(re.findall(r'(\d*)',item['buying_end'][0],re.M))
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
        
        item['live_time'] = "".join(item['live_time']).replace(u"天","").replace(u"年","x365").replace(" ","")
        if not item['live_time']:
            item['live_time'] = "0"
        item['live_time'] = item['live_time'].split("x")
        if len(item['live_time']) == 2:
            item['live_time'] = int(item['live_time'][0]) * int(item['live_time'][1])
        else:
            item['live_time'] = item['live_time'][0]
        #利率
        
        item['std_rate'] = item['std_rate'][0].replace("%","").split("-")
        if len(item['std_rate']) ==2:
            item['std_rate'] = item['std_rate'][1]
        elif len(item['std_rate']) ==1:
            item['std_rate'] = item['std_rate'][0]
        else:
            item['std_rate'] = 0
        
        #风险等级
        item['risk_level'] = item['risk_level'].replace(u"较低","2").replace(u"较高","4") \
                                .replace(u"低","1").replace(u"中","3").replace(u"高","5")
        item['risk_level'] = re.findall(r'(\d)',item['risk_level'],re.M)[0]  
       
        return item