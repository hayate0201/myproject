#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,codecs,json,collections,time,re

class pipline():

    def process(self,item):
        if len(item['prod_type']) >0:
            item['prod_type'] = item['prod_type'][0]
        return item
        
BASE_PATH = "F:\Github/myproject/myproject/pip"
self_dir = os.path.join(BASE_PATH,"demo.json")
self_file = codecs.open(self_dir, 'wb+', encoding='utf-8')
self_file.write("")#清空文件内容
# 打开文件
fo = open("F:\Github/myproject/data/bank_pingan.json", "r")
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

