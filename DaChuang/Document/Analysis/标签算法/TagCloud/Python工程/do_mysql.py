#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import MySQLdb
reload(sys)
sys.setdefaultencoding("utf-8")

###############################使用前配置表选择表###################################
table_name = 'nwpu_news'
########################################################################

####################常量###########
stopword_path = 'stop_words.txt'
####################常量###########

conn = MySQLdb.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = 'root',
    db = 'dcspider',
    charset = "utf8",
)
cur = conn.cursor()
cur.execute("SET NAMES utf8")

aa = cur.execute("select title from %s" % (table_name))
info = cur.fetchmany(aa)

for ii in range(len(info)):
    sql = 'update %s set id = %d where title = "%s"' % (table_name , ii+1 , info[ii][0])
    try:
        print sql
        cur.execute(sql)
        conn.commit()
    except:
        conn.rollback()

###########################将停用词写入数据库#####################################
''''
with open('stop_words.txt' , 'rb') as f:
    text = f.readlines()

for ii in text:
    ii1 = ii.decode('gbk')
    ii2 = ii1.encode('utf-8')
    sql1 = 'insert into stop_words (words) values ("%s")' % (ii2)
    try:
        cur.execute(sql1)
        conn.commit()
    except:
        conn.rollback()
'''
#########################将停用词写入数据库结束#########################################################

''' # 修改热词表的ID
str1 = cur.execute("select id from hot_words")
info = cur.fetchmany(str1)
aa = list(info)
for ii in range(str1):
    sql = 'update hot_words set id = %d where id = %d' % (ii+1,list(aa[ii])[0])
    try:
        cur.execute(sql)
        conn.commit()
        print sql
    except:
        conn.rollback()
'''

''''
# ####################一些数据库操作###########################
a = len(info)
for ii in range(a):
    sqll = 'update train set id = %d where title = "%s"' % (ii,info[ii][0])
    try:
        cur.execute(sqll)
        conn.commit()
    except:
        conn.rollback()
'''''

# ####################关键字词典打印###########################
'''
# 关键字词典按重要度排序
dict_hot_word_list = sorted(dict_hot_word.iteritems() , key=lambda asd:asd[1] , reverse=True)

for ii in dict_hot_word_list:
    sqll = 'insert into hot_words (words,value) values ("%s",%f)' % (ii[0] , ii[1])
    try:
        cur.execute(sqll)
        conn.commit()
        print ii[0] , ii[1]
    except:
        conn.rollback()
'''
# ####################关键字词典打印结束###########################
conn.close()