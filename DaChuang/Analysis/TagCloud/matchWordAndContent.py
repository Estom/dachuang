#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# 脚本名称：matchWordAndContent.py
# 脚本作用：将文章与热词联系在一起
"""
import sys
import SQLconfig
import FormatData
from sklearn.feature_extraction.text import TfidfVectorizer
reload(sys)
sys.setdefaultencoding("utf-8")

Data_content = []
Data_ID = []
i = 0
while True:
    info = SQLconfig.sql1.select('dcweb_article', ['id', 'title', 'content'], None, 1, i)
    if len(info) == 0:
        break
    Data_ID.append(info[0])
    Data_content.append(FormatData.TextCut(info[1]*2 + info[2]))
    i += 1
    print "读取第%d条数据" % i
numcontent = i  # 文章数目

# 读热词
dict_hot_word = {}  # 所有的关键词列表
i = 0
while True:
    info = SQLconfig.sql1.select('dcweb_tag', ['name', 'id'], None, 1, i)
    if len(info) == 0:
        break
    dict_hot_word.update({info[0]: info[1]})
    i += 1
    print "读取第%d条数据" % i

# 读取停用词表
stpwrdlst = []
with open('stop_words.txt', 'rb') as f:
    text = f.readlines()
for ii in text:
    ii1 = ii.decode('utf8')
    ii1 = ii1.strip("\r\n")
    stpwrdlst.append(ii1)
# 读停用词表结束

'''得到文章的关键词'''
FeaturesWordList = []      # 文章的关键词列表
dict = {}                  # 中间变量
dict_1 = []                # 中间变量
# 文章Tfidf化
vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.2)
tfidf = vectorizer.fit_transform(Data_content)
stopwords = vectorizer.get_stop_words()
word = vectorizer.get_feature_names()
weight = tfidf.toarray()
for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"
    dict.clear()
    dict_1 = []
    for j in range(len(word)):
        if weight[i][j] > 0.1:  # 如果一个词的Tfidf值大于0.1才进入统计列表
            dict.update({word[j]: weight[i][j]})
    dict_1 = sorted(dict.iteritems(), key=lambda asd: asd[1], reverse=True)
    dict.clear()
    for ii in dict_1:
        if len(dict) < 5:
            dict.update({ii[0]: ii[1]})
    FeaturesWordList.append(dict.items())
'''以上程序已经所有文章关键词的提取'''

# #######################文章与关键词匹配###############################
for ii in range(numcontent):
    for jj in FeaturesWordList[ii]:
        id_tag = dict_hot_word.get(jj[0])
        dic = {'article_id': Data_ID[ii], 'tag_id': id_tag}
        SQLconfig.sql1.add('dcweb_article_tag', dic)
        if Data_ID[ii] is not None and id_tag is not None:
            print '文章号 : %d , 标签号 : %d' % (Data_ID[ii], id_tag)
# #######################文章与关键词匹配##################################
