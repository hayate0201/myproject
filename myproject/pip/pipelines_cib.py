# -*- coding: utf-8 -*-
#兴业

import os,codecs,json,collections,time,re
from scrapy.conf import settings

class CibPipeline(object):
    def process_item(self, item, spider):
        #起购金额
        item['start_amount'] = int(float(item['start_amount'].replace(",","")))
        
        #货币类型
        item['coin_type'] = "人民币"
        #产品类型
        item['prod_type'] = "非保本浮动收益型"
        
        #周期
        item['live_time'] = re.findall(r'(\d*)',item['live_time'],re.M)[0]
        if not item['live_time']:
            item['live_time'] = 0
        
            
        #购买时间
        item['buying_start'] = re.findall(r'(\d*-\d*-\d*)',item['buying_start'],re.M)
        item['buying_end'] = re.findall(r'(\d*-\d*-\d*)',item['buying_end'],re.M)
        if len(item['buying_start']) ==0:
            item['buying_start'] = 0
        else:
            item['buying_start'] = int(time.mktime(
                time.strptime(item['buying_start'][0], '%Y-%m-%d')
                ))

        if len(item['buying_end']) == 0:
            item['buying_end'] = 0
        else:
            item['buying_end'] = int(time.mktime(
                time.strptime(item['buying_end'][0], '%Y-%m-%d')
                ))
        #风险等级
        item['risk_level'] = item['risk_level'].replace(u"较低风险","2").replace(u"较高风险","4")\
                            .replace(u"中风险","3").replace(u"低风险","1").replace(u"高风险","5")\
                            .replace(u"基本无风险","1")
        #利率
        item['std_rate'] = item['std_rate']
        
        
        return item
