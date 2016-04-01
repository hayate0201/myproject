# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #自增编码，爬取数据不建议使用自增id
    bank_code=scrapy.Field()#银行编码
    bank_name=scrapy.Field()#银行名称
    bank_type=scrapy.Field()#银行类型：国有上市，区域上市，网络公司
    prod_code = scrapy.Field()#产品编码
    prod_name = scrapy.Field()#产品名称
    prod_type = scrapy.Field()#产品类型：理财产品，基金，信托等
    start_amount = scrapy.Field()#起购金额
    live_time = scrapy.Field()#周期
    std_rate = scrapy.Field()#利率
    risk_level=scrapy.Field()#风险等级
    create_time=scrapy.Field()#抓取时间
    status = scrapy.Field()#状态
    total_type=scrapy.Field()#全部数据类型：XML,JSON,HTML,ARRAY
    total_data=scrapy.Field()#全部数据

product = MyprojectItem(prod_name='Desktop PC', risk_level=1000)
#print product