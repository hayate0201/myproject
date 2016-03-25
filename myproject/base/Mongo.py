__author__ = 'apple'
#-*-coding:utf-8-*-
import pymongo
class mongo():
    def __init__(self,host,port,dbname,collection):
        self.conn = pymongo.MongoClient(host,port)
        self.db = self.conn[dbname]
        self.obj= self.db[collection]
        print self.obj
        data={"rootz":"yangxiz"}
        self.obj.save(data)
    def object(self,collection):
        if collection:
            return self.db[collection]
        else:
            return self.obj
    #用SQL标准的方式进行初级封装
    def insert(self,data,type=False):
        a=self.obj.save(data)
    #用SQL标准的方式进行初级封装
    def update(self,data,type=False):
        self.obj.update(data)
    #用SQL标准的方式进行初级封装
    def delete(self,data,type=False):
        self.obj.remove(data)

if __name__=='__main__':
    a=mongo('localhost',27017,'local','test')
    test = {"rootkkk3":"yangxikkk3"}
    mg=a.object("test1")

    mg.save(test)
    test1 = {"rootkkks":"yangxikkks"}
    a.insert(test1)


