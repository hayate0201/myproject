# -*- coding: utf-8 -*-
#中国银行数据处理

import os,codecs,json,collections,time,re
from scrapy.conf import settings

class BocPipeline(object):
    def process_item(self, item, spider):
        #产品名字
        item['prod_name'] = item['prod_name'].replace("\"","")
        #货币类型
        if not item['coin_type']:
            item['coin_type'] = "".join(re.findall(ur'(美元)|(英镑)|(澳元)|(港币)',item['prod_name'],re.M)[0])
        #起购金额
        item['start_amount'] = item['start_amount'].replace(u"万","0000").replace(",","")
        item['start_amount'] = ' '.join(re.findall(r'\d*',item['start_amount'],re.M)).replace(" ","")
        #购买时间
        
        
        if item['buying_start'] != "":
            item['buying_start'] = item['buying_start'].replace("/","").replace("-","")
            item['buying_end']   = item['buying_end'].replace("/","").replace("-","")
            item['buying_start'] = int(time.mktime(
                time.strptime(str(item['buying_start']), '%Y%m%d')
                ))
            item['buying_end'] = int(time.mktime(
                time.strptime(str(item['buying_end']), '%Y%m%d')
                ))
        else:
            item['buying_start'] = 0
            item['buying_end'] = 0
     
        item['live_time'] = item['live_time'].replace(u"无固定存续期限","0").replace(" ","").replace(u"≤","").replace("+","")
        if item['live_time'].isdigit():
            pass
        else:
            item['live_time'] = re.findall(r'T(\d*)',item['live_time'],re.M)[0]
        
        item['risk_level'] = item['risk_level'].replace(u"中低","2").replace(u"中高","4")\
                            .replace(u"中","3").replace(u"低","1").replace(u"高","5")
        #利率
        item['std_rate'] = item['std_rate'].replace(u"净值","0").replace("%","").replace(u"或","-")
        item['std_rate'] = item['std_rate'].split("-")[0]
        
        return item
