#encoding=utf-8
#���ݿ����
'''
import pymongo

conn = pymongo.MongoClient("127.0.0.1",27017)
db  = conn.test
content = db['bank_boc'].find()
print content
'''
import urllib2,urllib     # ���������⵼��

url = 'https://api.douban.com/v2/book/user/ahbei/collections'  # ����Ҫ�����url

data={'status':'read','rating':3,'tag':'С˵'}  # ����api�ĵ��ṩ�Ĳ�������������ȡһ�°������������У�������ˡ�С˵�������ǩ�������鼮������Щ����ֵ����һ��dict��

data = urllib.urlencode(data) # �Ѳ������б��� 

url2 = urllib2.Request(url,data) # ��.Request������POST����ָ������Ŀ����֮ǰ�������url���������ݷ���data��

response = urllib2.urlopen(url2)  # ��.urlopen����һ�����صĽ�����õ���������Ӧ����

apicontent = response.read()  #����Ӧ������read()��ȡ����

print  apicontent  #��ӡ��ȡ��������