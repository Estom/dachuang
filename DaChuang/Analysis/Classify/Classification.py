#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
脚本名称：Classification.py
脚本用作用：分类
"""
import sys
import FormatData
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
import SQLconfig
reload(sys)
sys.setdefaultencoding("utf-8")

# 提取数据+分词+建立Bunch数据
bunch = Bunch(contents=[], id=[])
date = []
i = -1
while True:
    i += 1
    state = SQLconfig.sql0.select('article', ['id', 'process_state'], None, 0, i)
    if len(state) == 0:
        break
    if (state[1] % 2**3)/(2**0) % 2 == 1:
        print "id = %d文章已完成分类" % state[1]
        continue
    else:
        cate = SQLconfig.sql0.select('article', ['category'], None, 1, i)
        if cate[0] in SQLconfig.dicClassToCategory.values():
            print "%d: id = %d 文章来源存在类别" % (i, state[0])
            continue
        else:
            info = SQLconfig.sql0.select('article', ['id', 'content'], None, 1, i)
            info[1] = FormatData.TextCut(info[1])
            date.append(info)
            bunch.contents.append(info[1])
            bunch.id.append(info[0])
            print "%d: id = %d 文章自动分类" % (i, state[0])
# 提取数据+分词+建立Bunch数据结束

# 读取停用词
stpwrdlst = FormatData.readfile(SQLconfig.stopword_path).splitlines()

# 导入训练数据的bunch数据
train_bunch = FormatData.readbunchobj(SQLconfig.wordbag_path)

# 构建tf-idf词向量空间对象
tfidfspace = Bunch(id=bunch.id, tdm=[], vocabulary={})
tfidfspace.vocabulary = train_bunch.vocabulary
# 构建使用TfidfVectorizer初始化向量空间模型
# 这里面有TF-IDF权重矩阵还有我们要的词向量空间坐标轴信息vocabulary_
test_vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5, vocabulary=train_bunch.vocabulary)
# 此时tdm里面存储的就是if-idf权值矩阵
tfidfspace.tdm = test_vectorizer.fit_transform(bunch.contents)

# 导入分类器
# clf = MultinomialNB(alpha=0.001).fit(train_bunch.tdm, train_bunch.label)
clf = FormatData.readbunchobj(SQLconfig.classification_path)
predicted = clf.predict(tfidfspace.tdm)

i = 0
for id, expct_cate in zip(tfidfspace.id, predicted):
    i = i + 1
    dic = {'category': expct_cate}
    SQLconfig.sql0.update('article', dic, 'id = %d' % id)
    print "存第%s条数据！" % i
