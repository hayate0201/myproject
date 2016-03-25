__author__ = 'apple'
#-*-coding:utf-8-*-

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
#这里改为你的爬虫类名
#from spiders.cmbc import CmbcSpider
from spiders.cmbc import CmbcSpider

spider = CmbcSpider()
settings = get_project_settings()
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
log.start()
reactor.run()