#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
# 脚本名称：gethotword.py
# 脚本作用：统计热词
# 备 注：用户需要手动改变数据表的名称 
'''

###############################使用前配置表选择表#########################
table_name = 'nwpu_news'
# table_name = 'shool_news'
# table_name = 'wechat_article'
########################################################################

####################常量###########
title_name = 'title'       # 在表中文章标题的名字
content_name = 'content'   # 在表中文章内容的名字
id_content_name = 'id'     # 在表中文章id的名字
stopword_path = 'stop_words.txt'
####################常量###########

if (table_name  == 'wechat_article'):
    content_name = 'content_real'

import sys
import MySQLdb
from sklearn.feature_extraction.text import TfidfVectorizer
reload(sys)
sys.setdefaultencoding("utf-8")
import FormatData

'''
# 代码执行流程：
# 先读取文章内容再更新热词
# 两步最好不要交叉
'''

# 连接数据库
conn = MySQLdb.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    passwd = 'ykl123',
    db = 'dcdata',
    charset = "utf8",
)
cur = conn.cursor()
cur.execute("SET NAMES utf8")
str1 = cur.execute("select %s , %s from %s" % (title_name , content_name , table_name))
content = cur.fetchmany(str1)

# 读热词
hotword_cur = cur.execute("select words , value from hot_words")
info_hotword = cur.fetchmany(hotword_cur)
# 度热词结束

hotwordlist = []    # 本次数据库操作所有关键词的集合
for ii in info_hotword:
    hotwordlist.append(ii[0])

# 关键词列表
dict_hot_word = {}  # 所有的关键词列表
for ii in info_hotword:
    dict_hot_word.update({ii[0]:ii[1]})


Data = list(content)
Data_content = []

# 开始分词
for ii in range(len(Data)):
    Data[ii] = list(Data[ii])
    Data_content.append(FormatData.TextCut(Data[ii][0]*2 + Data[ii][1]))
# 分词结束

# 读取停用词表
stpwrdlst = []
with open('stop_words.txt' , 'rb') as f:
    text = f.readlines()
for ii in text:
    ii1 = ii.decode('utf8')
    ii1 = ii1.strip("\r\n")
    stpwrdlst.append(ii1)
# 读停用词表结束

'''用新文章更新热词词典，并记录新文章的热词'''
FeaturesWordList = []      # 文章的关键词列表
dict = {}                  # 中间变量
dict_1 = []                # 中间变量
# 文章Tfidf化
vectorizer = TfidfVectorizer(stop_words = stpwrdlst , sublinear_tf = True , max_df = 0.2)
tfidf = vectorizer.fit_transform(Data_content)
stopwords = vectorizer.get_stop_words()
word = vectorizer.get_feature_names()
weight = tfidf.toarray()
for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"
    dict.clear()
    dict_1 = []
    for j in range(len(word)):
        if (weight[i][j] > 0.1): # 如果一个词的Tfidf值大于0.1才进入统计列表
            dict.update({word[j] : weight[i][j]})
    dict_1 = sorted(dict.iteritems() , key=lambda asd:asd[1] , reverse=True)
    dict.clear()
    for ii in dict_1:
        if (len(dict) < 5):
            dict.update({ii[0]:ii[1]})
            if (dict_hot_word.has_key(ii[0])):
                dict_hot_word.update({ii[0] : ii[1] + dict_hot_word.get(ii[0])})
            else:
                dict_hot_word.update({ii[0] : ii[1]})
    FeaturesWordList.append(dict.items())
'''以上程序已经实现了热词的更新和当前数据表中文章关键字的提取'''

# #######################热词存回数据库###############################
dict_hot_word_list = sorted(dict_hot_word.iteritems() , key=lambda asd:asd[1] , reverse=True)
for ii in dict_hot_word_list:
    if (ii[0] in hotwordlist):  # 如果这条热词已经在数据库了就更新这个热词的权值
        sql = 'update hot_words set value = %f where words = "%s"' % (ii[1] , ii[0])
    else:
        sql = 'insert into hot_words (words , value) values("%s" , %f)' % (ii[0] , ii[1])
    try:
        cur.execute(sql)
        conn.commit()
        print ii[0], ii[1]
    except:
        conn.rollback()
# #######################热词存回数据库结束##################################

# 关闭数据库
conn.close()


