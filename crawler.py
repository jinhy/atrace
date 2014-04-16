# -*- coding: utf-8 -*-
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
import urllib2
from urllib2 import Request

DB='data/data.db'
url='https://www.ibm.com/developerworks/cn/linux/kernel/syscall/part1/appendix.html'

conn=sqlite3.connect(DB)
db = conn.cursor()
db.execute("CREATE TABLE IF NOT EXISTS syscall (id INTEGER PRIMARY KEY,name varchar NOT NULL, category varchar , description varchar)")

db.execute('delete from syscall where 1=1')

data=urllib2.urlopen(url).read()
soup = BeautifulSoup(data)
f=open('data/123.txt','w')
for table in soup.findAll('table','ibm-data-table'):
    p=table.findPreviousSibling('p')
    for tr in table.findAll('tr'):
        tds=tr.findAll('td')
        sql="INSERT INTO syscall (name,category,description) VALUES ('"+tds[0].text+"','"+p.text[2:]+"','"+tds[1].text+"')"
        f.write(p.text[2:]+' '+tds[0].text+' '+tds[1].text+'\n')
        db.execute(sql);
conn.commit()
#db.execute("SELECT id, name,category,description FROM syscall WHERE name = 'getpid'")
#result = db.fetchone()
#print result[1]
#for t in result:
#    print t
'''con.execute("CREATE TABLE IF NOT EXISTS syscall (id INTEGER PRIMARY KEY,name varchar NOT NULL, category varchar NOT NULL, description varchar NOT NULL)")
con.execute("INSERT INTO syscall (name,category,description) VALUES ('a','b','c')")
con.execute("INSERT INTO syscall (name,category,description) VALUES ('a2','b2','c2')")
con.commit()'''
db.close()
