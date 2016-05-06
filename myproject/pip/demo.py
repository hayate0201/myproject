#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,codecs,json,collections,time,re

class pipline():

    def process(self,item):
        #start_amount
        item['start_amount'] = int(float(item['start_amount'].replace(",","")))
        
        #购买周期
        try:
            item['buying_start'] = int(time.mktime(
                    time.strptime(item['buying_start'], '%Y/%m/%d')
                    ))
        except:
            item['buying_start'] = 0
            
        try:
            item['buying_end'] = int(time.mktime(
                    time.strptime(item['buying_end'], '%Y/%m/%d')
                    ))
        except:
            item['buying_end'] = 0
            
        #周期
        live_time = item['live_time'].replace(u"天","").replace("-","")
        item['live_time'] = live_time if live_time else "0"
        
        #利率
        std_rate = re.findall(r'(\d*\.\d*)%',item['std_rate'],re.M)
        item['std_rate'] = std_rate[0] if std_rate else "0"
        return item
        
BASE_PATH = "F:\Github/myproject/myproject/pip"
self_dir = os.path.join(BASE_PATH,"demo.json")
self_file = codecs.open(self_dir, 'wb+', encoding='utf-8')
self_file.write("")#清空文件内容
# 打开文件
fo = open("F:\Github/myproject/data/bank_spdb.json", "r")
print u"文件名为: ", fo.name
line = fo.readlines()
obj = json.dumps(line)
obj = json.loads(obj)
for i in obj:
    item = json.loads(i)
    item = pipline().process(item)
    line = json.dumps(collections.OrderedDict(item)) + "\n"
    self_file.write(line.decode("unicode_escape")) 

# 关闭文件
fo.close()

