# -*- coding: utf-8 -*-
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import string
import re
DB='data/data.db'
conn=sqlite3.connect(DB)
db = conn.cursor()
print 'loading LSB func...'
cc=0

for line in open('lsb','r').readlines():
	for funcs in  re.split('\t',line.strip() ):
		funcs=re.sub('\(.*\)','',funcs).strip()
		m=re.split('\[',re.sub('\'\"','',funcs))
		if len(m)<2:
			continue
		sql="select * from data where category='libc' and name='"+m[0].strip()+"'"
		db.execute(sql)
		if len(db.fetchall())<1:
			sql="INSERT INTO data (name,OSv,category,function,description) VALUES ('"+m[0]+"','0','libc','unknown','"+m[1][:-1]+" function')"
			db.execute(sql)
			cc=cc+1
conn.commit()
print 'done , add total = ',cc
