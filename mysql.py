#encoding=utf-8
#数据库测试
import time, MySQLdb 


#连接      
conn = MySQLdb.connect(host="localhost",user="root",passwd="31480212",db="test",charset="utf8")    
cursor = conn.cursor() 

#创建  
#sql = "create table if not exists user(name varchar(128) primary key, created int(10))"  
#cursor.execute(sql)  

#写入多行      
sql = "insert into user(name,created) values(%s,%s)"     
param = (("bbb",int(time.time())), ("ccc",33), ("ddd",44) )  
#n = cursor.executemany(sql,param)      
#print 'insertmany',n  

#查询      
n = cursor.execute("select * from user")      
print cursor.fetchall()   