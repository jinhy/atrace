# -*- coding: utf-8 -*-
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from bs4 import BeautifulSoup
import urllib2
from urllib2 import Request
import string
import re
DB='data/data.db'
conn=sqlite3.connect(DB)
db = conn.cursor()
print 'loading gunlib func...'
cc=0
base_url='http://pubs.opengroup.org/onlinepubs/009695399/idx/i'
for word in string.lowercase:
	url=base_url+word+'.html'
	print word
	data=urllib2.urlopen(url).read()
	soup = BeautifulSoup(data)
	for li in soup.find('ul').findAll('li'):
		m=re.match('(.*?)\s*-\s*(.*)',li.text.strip())
		names=re.sub('[\(\),\\\'\"]','',m.group(1)).strip()
		description=re.sub('[\\\'\"]','',m.group(2)).strip()
		if re.search('\.',names):
			continue
		for name in [n for n in re.split('\s*',names)]:
			sql="select * from data where category='libc' and name='"+name+"'"
			db.execute(sql)
			if len(db.fetchall())<1:
				sql="INSERT INTO data (name,OSv,category,function,description) VALUES ('"+name+"','0','libc','unknown','"+description+"')"
				#print sql
				db.execute(sql)
				cc=cc+1
conn.commit()
print 'done , add total = ',cc
