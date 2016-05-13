# -*- coding: utf-8 -*-
#农行数据处理

import os,codecs,json,collections,time,re
from scrapy.conf import settings

class AbcPipeline(object):
    def process_item(self, item, spider):
        #起购金额
        item['start_amount'] = int(float(item['start_amount']))
        #购买时间
        if item['buying_start'] != "":
            item['buying_start'] = int(time.mktime(
                time.strptime(item['buying_start'], '%Y/%m/%d')
                ))
            item['buying_end'] = int(time.mktime(
                time.strptime(item['buying_end'], '%Y/%m/%d')
                ))
        else:
            item['buying_start'] = 0
            item['buying_end'] = 0
        #利率
        item['std_rate'] = item['std_rate'].replace("%","").split("-")
        if len(item['std_rate']) ==2:
            item['std_rate'] = item['std_rate'][1]
        elif len(item['std_rate']) ==1:
            item['std_rate'] = item['std_rate'][0]
        else:
            item['std_rate'] = 0
        #风险等级
        item['risk_level'] = item['risk_level'].replace(u"中低","2").replace(u"中高","4") \
                        .replace(u"低","1").replace(u"中","3").replace(u"高","5")
        #收益周期
        item['live_time'] = ' '.join(re.findall(r'\d*',item['live_time'],re.M)).replace(" ","")
        #产品类型

        #货币类型
        return item
