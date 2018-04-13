#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
脚本名称：Classification.py
脚本用作用：分类
"""
import sys
import os
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)
print path
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
import Analysis.SQLconfig
import Analysis.FormatData
reload(sys)
sys.setdefaultencoding("utf-8")


def RunClassify():
    """
    分类算法入口
    :return: 无
    """
    # 提取数据+分词+建立Bunch数据

    continue_flag = True
    # 取数据操作的改变，直接搜索语句就好了
    while continue_flag:
        bunch = Bunch(contents=[], id=[])
        info = Analysis.SQLconfig.sql0.select('article', ['id', 'content'], 'category is null', 1000, None)
        if len(info) == 0:
            print u"已完成全部分类"
            return
        if len(info) < 1000:
            continue_flag = False
        for ii in info:
            bunch.id.append(ii[0])
            bunch.contents.append(ii[1])
        print u"已读%d条数据" % len(info)

        # 读取停用词
        stpwrdlst = Analysis.FormatData.readfile(Analysis.SQLconfig.stopword_path).splitlines()

        # 导入训练数据的bunch数据
        train_bunch = Analysis.FormatData.readbunchobj(Analysis.SQLconfig.wordbag_path)

        # 构建tf-idf词向量空间对象
        tfidfspace = Bunch(id=bunch.id, tdm=[], vocabulary={})
        tfidfspace.vocabulary = train_bunch.vocabulary
        # 构建使用TfidfVectorizer初始化向量空间模型
        # 这里面有TF-IDF权重矩阵还有我们要的词向量空间坐标轴信息vocabulary_
        test_vectorizer = TfidfVectorizer(stop_words=stpwrdlst, sublinear_tf=True, max_df=0.5,
                                          vocabulary=train_bunch.vocabulary)
        # 此时tdm里面存储的就是if-idf权值矩阵
        tfidfspace.tdm = test_vectorizer.fit_transform(bunch.contents)

        # 导入分类器
        clf = Analysis.FormatData.readbunchobj(Analysis.SQLconfig.classification_path)
        predicted = clf.predict(tfidfspace.tdm)

        i = 0
        for article_id, expect_cate in zip(tfidfspace.id, predicted):
            i = i + 1
            dic = {'category': expect_cate}
            Analysis.SQLconfig.sql0.update('article', dic, 'id = %d' % article_id)
            print u"存第%s条数据！" % i


if __name__ == '__main__':
    RunClassify()
