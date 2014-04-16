# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sqlite3
import re
import os
DB='data/data.db'
conn=sqlite3.connect(DB)
db = conn.cursor()

print 'loading osv libc...'
cc=0
elfile=os.popen('locate loader.elf').read().strip().split('\n')
if len(elfile)>0 and elfile[0].split('/')[-1] =='loader.elf':
	print 'finding syscall....'
	elfile=elfile[0]
	os.popen('objdump -t '+elfile+' > /tmp/a')
	db.execute("select name from data where category='libc'")
	result=[item[0].strip() for item in db.fetchall()]
	for func in result:
		find=os.popen('grep " '+func+'$" /tmp/a').read().strip()
		if len(find)>0:
			db.execute("update data set OSv=1 where category='libc' and name='"+func+"'")
			cc=cc+1
	conn.commit()
	print 'total libc funcs found = ',cc
	print 'loading osv syscall....'
	cc1=0
	cc2=0
	db.execute("select name from data where category='syscall'")
	result=[item[0].strip() for item in db.fetchall()]
	for func in result:
		db.execute("select name from data where category='libc' and name='"+func+"'")
		result=db.fetchall()
		find=os.popen('grep " '+func+'$" /tmp/a').read().strip()
		if len(find)>0:
			if len(result)>0:
				db.execute("update data set OSv=2 where category='syscall' and name='"+func+"'")
				cc2=cc2+1
			else:
				db.execute("update data set OSv=1 where category='syscall' and name='"+func+"'")
				cc1=cc1+1

	conn.commit()
	print 'total syscall found = ',cc1
	print cc2,' funcs found may be syscalls'
else:
	print 'loader.elf not found,try to make in osv dir'

