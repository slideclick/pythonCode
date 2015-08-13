import os, sys  
import MySQLdb  
import pymssql
import _mssql
try:  
    conn= MySQLdb.connect(host='localhost',user='root',passwd='',db='address'  )
    #    conn = _mssql.connect(server='10.10.10.10', user='user', password='xxx',                             database='dbname')
except Exception as e:  
    print (e  )
    sys.exit()  
cursor=conn.cursor()  # sql server need not cursor
sql='insert into address(name, address) values(%s, %s)'  
value=(('zhangsan','haidian'),('lisi','haidian'))  # tuple's tuple, INSERT 2 lines
try: 
    cursor.executemany(sql,values)  #conn.execute_query
except Exception as e:  
    print (e  )
sql='select * from address'  
cursor.execute(sql)  # single statement e.g. SELECT
data=cursor.fetchall()  
if data  :
    for x in data:  
        print (x[0],x[1]  )
cursor.close()  
conn.close() 