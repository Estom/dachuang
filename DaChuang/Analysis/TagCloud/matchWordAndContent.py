#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
# 脚本名称：matchWordAndContent.py
# 脚本作用：将文章与热词联系在一起
"""
import sys
import Analysis.SQLconfig
import Analysis.FormatData
from sklearn.feature_extraction.text import TfidfVectorizer
reload(sys)
sys.setdefaultencoding("utf-8")


def runmatchWordAndContent():
    break_flag = False
    index = -1001
    while True:
        index += 1000
        if break_flag:
            print "热词与文章匹配结束！！！！！！"
            break
        Data_content = []
        Data_ID = []
        num = 0
        while True:
            if num > 1000:
                print "一次最多处理1000条数据"
                break
            index += 1
            state = Analysis.SQLconfig.sql1.select('dcweb_article', ['id', 'tag_mark'], None, 1, index)
            if len(state) == 0:
                print "统计数据结束!!!!!"
                break_flag = True
                break
            if (state[1] % 2 ** 2) / 2 ** 1 % 2 != 1:
                print "%d:id = %d 文章未统计热词,不允许与热词匹配" % (index, state[0])
                continue
            if (state[1] % 2 ** 2) / 2 ** 0 % 2 == 1:
                print "%d:id = %d 文章已和热词匹配" % (index, state[0])
                continue
            else:
                num += 1
                info = Analysis.SQLconfig.sql1.select('dcweb_article', ['id', 'title', 'content'], None, 1, index)
                Data_ID.append([info[0], state[1]])
                Data_content.append(Analysis.FormatData.TextCut(info[1] * 2 + info[2]))
                print "%d:读取id = %d文章内容" % (index, state[0])
        numcontent = num  # 文章数目

        # 读热词
        dict_hot_word = {}  # 所有的关键词列表
        i = 0
        while True:
            info = Analysis.SQLconfig.sql1.select('dcweb_tag', ['name', 'id'], None, 1, i)
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
        FeaturesWordList = []  # 文章的关键词列表
        dict = {}  # 中间变量
        dict_1 = []  # 中间变量
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
                if dict_hot_word.has_key(jj[0]):
                    id_tag = dict_hot_word.get(jj[0])
                    value = jj[1] * 1000
                else:
                    continue
                if Data_ID[ii][0] is not None and id_tag is not None and value is not None:
                    dic = {'article_id': Data_ID[ii][0], 'tag_id': id_tag, 'value': value}
                    Analysis.SQLconfig.sql1.add('dcweb_article_tag', dic)
                    print '文章号 : %d , 标签号 : %d , 重要度 : %d' % (Data_ID[ii][0], id_tag, value)
            Analysis.SQLconfig.sql1.update('dcweb_article', {'tag_mark': Data_ID[ii][1] % 2 ** 2 + 2 ** 0},
                                  'id = %d' % Data_ID[ii][0])
            print "%d:id = %d 更新文章状态为%d" % (index - 1000 + ii, Data_ID[ii][0], Data_ID[ii][1] % 2 ** 2 + 2 ** 0)
            # #######################文章与关键词匹配##################################

