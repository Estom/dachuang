#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
# 脚本名称：matchWordAndContent.py
# 脚本作用：将文章与热词联系在一起
# 备 注：用户需要手动改变数据表的名称 
'''

###############################使用前配置表选择表#########################
# table_name = 'nwpu_news'
# table_name = 'shool_news'
table_name = 'wechat_article'
########################################################################

####################常量###########
title_name = 'title'       # 在表中文章标题的名字
content_name = 'content'   # 在表中文章内容的名字
id_content_name = 'id'     # 在表中文章id的名字
stopword_path = 'stop_words.txt'
tag_name = 'nwpu_news_tag'  # 文章与热词榜的关系
####################常量###########

if (table_name == 'nwpu_news'):
    tag_name = 'nwpu_news_tag'
elif (table_name == 'shool_news'):
    tag_name = 'shool_news_tag'
elif (table_name == 'wechat_article'):
    tag_name = 'wechat_article_tag'
    content_name = 'content_real'

import sys
import MySQLdb
from sklearn.feature_extraction.text import TfidfVectorizer
reload(sys)
sys.setdefaultencoding("utf-8")
import FormatData

'''
# 先读取文章内容匹配更新热词
'''

# 连接数据库
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
str1 = cur.execute("select %s , %s from %s" % (title_name , content_name , table_name))
content = cur.fetchmany(str1)

content_cur = cur.execute("select id from %s" % (table_name))
info_content = cur.fetchmany(content_cur)

# 读热词
hotword_cur = cur.execute("select id , words , value  from hot_words")
info_hotword = cur.fetchmany(hotword_cur)
# 度热词结束

hotwordlist = []    # 所有关键词的集合
for ii in info_hotword:
    hotwordlist.append(ii[1])

# 开始分词
Data = list(content)
Data_content = []
for ii in range(len(Data)):
    Data[ii] = list(Data[ii])
    Data_content.append(FormatData.TextCut(Data[ii][0]*2 + Data[ii][1]))
# 分词结束

# 读取停用词表
stpwrdlst = []
with open('stop_words.txt' , 'rb') as f:
    text = f.readlines()
for ii in text:
    ii1 = ii.decode('gbk')
    ii1 = ii1.strip("\r\n")
    stpwrdlst.append(ii1)
# 读停用词表结束

'''得到文章的关键词'''
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
        if (weight[i][j] > 0.1):# 如果一个词的Tfidf值大于0.1才进入统计列表
            dict.update({word[j]: weight[i][j]})
    dict_1 = sorted(dict.iteritems(), key=lambda asd: asd[1], reverse=True)
    dict.clear()
    for ii in dict_1:
        if (len(dict) < 5):
            dict.update({ii[0]:ii[1]})
    FeaturesWordList.append(dict.items())
'''以上程序已经所有文章关键词的提取'''

# #######################文章与关键词匹配###############################
for ii in range(len(info_content)):
    for jj in FeaturesWordList[ii]:
        id_hotword = hotwordlist.index(jj[0])
        sql1 = 'insert into %s (article_id,hot_word_id,content_value,tatol_value) values (%d , %d , %f , %f)'\
               % (tag_name, info_content[ii][0], info_hotword[id_hotword][0], jj[1], info_hotword[id_hotword][2])
        try:
            cur.execute(sql1)
            conn.commit()
            print info_content[ii][0], info_hotword[id_hotword][0]
        except:
            conn.rollback()
# #######################文章与关键词匹配##################################

# 关闭数据库
conn.close()

