# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sqlite3
import re
from xlrd import *

DB='data/data.db'
conn=sqlite3.connect(DB)
db = conn.cursor()
print 'loading pre data...'
w=open_workbook('Book1.xlsx')
cc=0
rs=w.sheet_by_index(3)
for i in range(1,rs.nrows):
	name=rs.row(i)[0].value.strip()
	category=str(rs.row(i)[1].value).strip()
	if not category=='libc':
		category=='syscall'
	db.execute("select * from data where name = '"+name+"'")
	result=db.fetchall()
	sql=""
	if len(result)>1:
		sql="update data set OSv = '1' where name = '"+name+"' and category='"+category+"'"
	elif len(result)==1:
		sql="update data set OSv = '1' where name = '"+name+"'"
	db.execute(sql)
	cc=cc+1
conn.commit()

print 'total=',cc
cc=0

rs=w.sheet_by_index(2)
for i in range(1,rs.nrows):
	name=rs.row(i)[0].value.strip()
	function=rs.row(i)[1].value.strip()
	db.execute("update data set function = '"+function+"' where name = '"+name+"' and category='syscall'")
	cc=cc+1
conn.commit()


print 'total=',cc
print 'done'
