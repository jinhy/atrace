# -*- coding: utf-8 -*-
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import getopt
import sqlite3
from lib.bottle import  run, route, get,request,static_file,abort,install,template
from xlrd import *
from xlwt import *

DEBUG=0
root_dir=''
SO=0
opts, args = getopt.getopt(sys.argv[1:], "d:i:o:l:e:s:f")
#print opts
#print args
for o,v in opts:
    if o=='-d':
        root_dir=v
    elif o=='-f':
        SO=1

BROWSER="firefox"
STRACE_DIR=root_dir+"/data/tmp"
if DEBUG :
    BROWSER="chrome"
STATIC_DIR=root_dir+'/static'
DB=root_dir+'/data/data.db'

conn=sqlite3.connect(DB)
db = conn.cursor()

def sortself(item_list,col_list):
    for col in col_list:
        item_list=sorted(item_list,key=lambda item_list:item_list[col])
    return item_list
def get_info(item_list,category='syscall'):
    title=[]
    found=[]
    unfound=[]
    if len(item_list)<1:
        db.execute("PRAGMA table_info(data)")
        for item in db.fetchall():
            title.append(item[1])
        return {'title':title}
    filterc=""
    if category=='libc':
        filterc=" and category = 'libc' "
    for item in item_list:
        sql="SELECT * FROM data WHERE name = '"+item+"' "+filterc+" order by OSv desc"
        db.execute(sql)
        line=db.fetchone()
        if line:
            found.append(line)
            title=[tuple[0] for tuple in db.description]
        else:
            unfound.append(item)
    return {'title':title,'found':sortself(found,[3,2]),'unfound':unfound}

def set_info(item_dic):
    sql1=""
    sql2=""
    sql=""
    sql="SELECT * FROM data WHERE name='" + item_dic['name'] + "'"
    db.execute(sql)
    flag=db.fetchall()
    if flag:
        for key,value in item_dic.items():
            sql1=sql1+','+key+"='" + value + "'"
        sql="UPDATE data SET " + sql1[1:] + " WHERE name = '" + item_dic['name'] + "'"
    else:
        for key,value in item_dic.items():
            sql1=sql1+','+key
            sql2=sql2+','+"'"+value+"'"
        sql="INSERT INTO data (" + sql1[1:] + ") VALUES (" + sql2[1:]+ ")"
    db.execute(sql)
    conn.commit()
    return "success"

def delete_info(item_list):

    for item in item_list:
        sql="DELETE FROM data WHERE name = '"+item+"'"
        db.execute(sql)
    conn.commit()
    return "success"

def all_info():
    title=[]
    found=[]
    unfound=[]
    sql="SELECT * FROM data"
    db.execute(sql)
    found=db.fetchall()
    if found:
        title=[tuple[0] for tuple in db.description]
    return {'title':title,'found':sortself(found,[3,2,1]),'unfound':unfound}

def oweb(result1,page):
    f=open(page,"w")
    f.write(template(STATIC_DIR+'/oweb.tpl',result=result1))
    f.close()
    os.system(BROWSER+" "+page)

def oexcel(result,file):
    w = Workbook(encoding='utf-8')
    ws = w.add_sheet('func')
    for i in range(1,len(result['title'])):
        ws.write(0,i-1,result['title'][i])
    for i in range(0,len(result['found'])):
        for j in range(1,len(result['title'])):
            ws.write(i+1,j-1,result['found'][i][j])
    pos=len(result['found'])
    for i in range(0,len(result['unfound'])):
        ws.write(i+pos+1,0,result['unfound'][i])
        ws.write(i+pos+1,1,"unfound")
    w.save(file)

def otxt(result,file):
    f=open(file,'w')
    keys=result['title']
    vals=result['found']
    for key in keys[1:]:
        f.write(""+key+'\t\t')
    f.write('\n')
    for item in vals:
        for val in item[1:]:
            f.write(str(val)+'\t\t')
        f.write('\n')
    for val in result['unfound']:
        f.write(val+'\t\tunfound\n')
    f.close()

def iexcel(file,category='syscall'):
    w = open_workbook(file)
    rs = w.sheet_by_index(0)
    keys=rs.col_values(0)
    return get_info([w.strip() for w in keys],category)

def itxt(file,category='syscall'):
    return get_info([line.strip() for line in open(file,'r')],category)

def idefault(file,category='syscall'):
    item_list=[]
    for line in open(file).readlines()[2:-2]:
        s=re.split('\s*',line.strip())[-1]
        item_list.append(s)
    return get_info(item_list,category)


def lexcel(file):
    w = open_workbook(file)
    rs = w.sheet_by_index(0)
    keys=rs.row_values(0)
    for i in range(1,rs.nrows):
        item={}
        for j in range(0,rs.ncols):
            item[keys[j].strip()]=rs.cell(i,j).value
        set_info(item)

def ltxt(file):
    f=open(file,'r')
    keys=f.readline().strip()
    keys=re.split('\t*',keys)

    for line in f.readlines():
        vals=re.split('\t*',line.strip())
        item={keys[i]:vals[i] for i in range(0,len(keys))}
        set_info(item)
    f.close()

def eweb(file):
    oweb(all_info(),file)

def eexcel(file):
    oexcel(all_info(),file)

def etxt(file):
    otxt(all_info(),file)

def getlibc():
    item_list=[]
    for sofile in args:
        funcs=os.popen('objdump -T '+sofile+' | grep GLIBC|sed -e "s/.*GLIBC_[0-9.]* //"').read().strip().split('\n')
        item_list.extend([func.strip() for func in funcs])
    return get_info(item_list,'libc')
def default():
    run(host = '127.0.0.1' , port = 80)


@route('/static/<filepath:path>')
def staticfile(filepath):
    global STATIC_DIR
    return static_file(filepath,root=STATIC_DIR)


@route('/')
def hello():
    return template(STATIC_DIR+'/syscalls.tpl',result=all_info())

@route('/u')
def update():
    query = request.GET.get('name',default = "")
    if query =="":
        return template(STATIC_DIR+'/update.tpl',result={},name="")
    return template(STATIC_DIR+'/update.tpl',result=get_info([query]),name=query)
        
@route('/i')
def insert():
    return template(STATIC_DIR+'/insert.tpl',result=get_info([]))
        
@route('/get')
def getData():
    query = request.GET.get('name',default = "")
    #print(query+' '+' '+lat+' ' + lng+'test')
    if not query:
        return "error"
    return get_info([query])

@route('/set')
def setData():        
    query = request.GET.get('name',default = "")
    if not query:
        return "error"
    item_dic={}
    for key,value in request.GET.items():
        item_dic[key]=value
    return set_info(item_dic)

@route('/delete')
def deleteData():
    query = request.GET.get('name',default = "")
    if not query:
        return "error"
    return delete_info([query])

le=0
for o,v in opts:
    if o == "-l":
        le=1
        if v.endswith('xls'):
            lexcel(v)
        else:
            ltxt(v)
    elif o == "-e":
        le=1
        if v.endswith('xls'):
            eexcel(v)
        elif v.endswith('html') or v.endswith('htm'):
            eweb(v)
        else:
            etxt(v)
if SO == 0:
    result={}
    ifile=""
    ofile=""
    for o,v in opts:
        if o == "-i":
            ifile=v
        elif o =="-o":
            ofile=v
    if ifile =="":
        result=idefault(STRACE_DIR)
    elif ifile !="":
        if ifile.endswith('xls'):
            result=iexcel(ifile)
        else:
            result=itxt(ifile)
    if ofile == "" and len(args) == 0 and ifile =="" and not le:
        default()
    elif ofile != "" and ofile.endswith('xls'):
        oexcel(result,ofile)
    elif (ofile != "" and ( ofile.endswith('html') or ofile.endswith('htm'))) or ( ofile =="" and (len(args)>0 or ifile !="")):
        if(ofile==""):
            oweb(result,"syscall.html")
        else:
            oweb(result,ofile)
    elif ofile != "" :
        otxt(result,ofile)
else:
    result={}
    ofile=""
    for o,v in opts:
        if o =="-o":
            ofile=v
    result=getlibc()
    if ofile.endswith('xls'):
        oexcel(result,ofile)
    elif ofile.endswith('html') or ofile.endswith('htm'):
        oweb(result,ofile)
    elif ofile != "" :
        otxt(result,ofile)
    else:
        oexcel(result,'libctest.xls')
