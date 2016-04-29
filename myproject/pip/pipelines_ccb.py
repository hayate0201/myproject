# -*- coding: utf-8 -*-
#建设银行数据处理

import os,codecs,json,collections,time,re
from scrapy.conf import settings

class CcbPipeline(object):
    def process_item(self, item, spider):
        #起购金额
        item['start_amount'] = int(item['start_amount'])
        
        #货币类型
        if item['coin_type'] == "01":item['coin_type'] = "人民币"
        elif item['coin_type'] == "12":item['coin_type'] = "英镑"
        elif item['coin_type'] == "13":item['coin_type'] = "港币"
        elif item['coin_type'] == "14":item['coin_type'] = "美元"
        elif item['coin_type'] == "15":item['coin_type'] = "瑞士法郎"
        elif item['coin_type'] == "27":item['coin_type'] = "日元"
        elif item['coin_type'] == "28":item['coin_type'] = "加元"
        elif item['coin_type'] == "29":item['coin_type'] = "澳元"
        elif item['coin_type'] == "33":item['coin_type'] = "欧元"
        else:
            item['coin_type'] = "其他"
            
        #购买时间
        if item['buying_start']:
            item['buying_start'] = item['buying_start']/1000
            item['buying_end'] = item['buying_end']/1000
        else:
            item['buying_start'] = 0
            item['buying_end'] = 0
            
        #风险等级
        item['risk_level'] = item['risk_level'].replace("0","")
        
        #产品类型
        if item['prod_type'] == "1":
            item['prod_type'] = "保证收益型"
        else:
           item['prod_type'] = "非保本浮动收益型"
           
        return item
