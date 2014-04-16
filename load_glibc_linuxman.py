# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sqlite3
import re
DB='data/data.db'
conn=sqlite3.connect(DB)
db = conn.cursor()
db.execute('DROP TABLE data')
db.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY,name varchar NOT NULL, OSv int ,category varchar , function varchar ,description varchar)")
db.execute('delete from data where 1=1')
print 'loading linux syscall...'
cc=0
for line in open('ab','r').readlines():

	if re.match('^top\s*$',line) or len(line.strip()) == 0:
		continue

	
	line=re.sub('[\'\"]','',line)
	m=re.match('\s*(.*)\((.*)\)\s*-\s*(.*)',line.strip())
	if m:
		#f.write(m.group(1)+'& '+m.group(2)+'& '+m.group(3)+'\n')
		category='unknown'
		function='unknown'
		name=m.group(1).strip()
		description=m.group(3).strip()
		if m.group(2).strip()=='2':
			category='syscall'
		elif m.group(2).strip()=='3':
			category='libc'
		sql="INSERT INTO data (name,OSv,category,function,description) VALUES ('"+name+"','0','"+category+"','"+function+"','"+description+"')"
		#print sql
		db.execute(sql)
		cc = cc+1
	else:
		print line
conn.commit()
print 'loading linux man...'

cc2=0
for line in open('gnu','r').readlines():
    line=re.sub('[\'\"]','',line).strip()
    m=re.match('(.*):(.*)',line.strip())
    if m:
        #f.write(m.group(1)+'& '+m.group(2)+'& '+m.group(3)+'\n')
        category='libc'
        function='unknown'
        name=m.group(1).strip()
        description=m.group(2).strip()
        sql="select * from data where name='"+name+"' and category='libc'"
        db.execute(sql)
        if len(db.fetchall())>0:
            continue
        sql="INSERT INTO data (name,OSv,category,function,description) VALUES ('"+name+"','0','"+category+"','"+function+"','"+description+"')"
        db.execute(sql)
        cc2 = cc2+1
    else:
        print line
conn.commit()
print cc,cc2
print 'done'

