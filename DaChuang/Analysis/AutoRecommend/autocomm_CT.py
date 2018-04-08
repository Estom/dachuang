# encoding=utf-8

"""
基于关键字的智能推荐算法
"""

# 给出需要推荐用户的id

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

def Commend_CT(UserID, numHistoryArticle=3, numTagRecommend=3, numRecommend=10):
    """
    基于关键字的智能推荐
    :param UserID: 推荐对象的ID
    :param numHistoryArticle: 根据用户的阅读的最近numHistoryArticle篇文章推荐
    :param numTagRecommend: 每个关键字推荐numTagRecommend篇文章
    :param numRecommend: 一次向用户推荐numRecommend篇文章
    :return: 在数据库更新目标用户的推荐列表
    """
    # 提取用户阅读记录
    import Analysis.SQLconfig
    ReadHistory = []
    ReadHistory.append(Analysis.SQLconfig.sql1.select('dcweb_history', ['article_id', 'time'],
                                             'user_id = %d' % (UserID), 10))
    ReadHistory = ReadHistory[0]
    # 用户阅读记录按阅读实现正序排序
    ReadHistory = sorted(ReadHistory, key=lambda x: (x[1]), reverse=True)
    # 找出用户最近阅读三篇文章的所有关键字
    tag_id = []
    for i in range(len(ReadHistory)):
        if i > numHistoryArticle - 1:  # 只找用户最近三篇文章的所有关键字
            break
        temp = Analysis.SQLconfig.sql1.select('dcweb_article_tag', ['tag_id', 'value'],
                                     'article_id = %d' % (ReadHistory[i][0]))
        temp = sorted(temp, key=lambda x: (x[1]), reverse=True)
        for ii in range(len(temp)):
            if ii > numTagRecommend - 1:
                break
            tag_id.append(temp[ii][0])
    # 找出用户阅读记录关键字的所有文章ID
    RecommendArticleId = []
    for i in tag_id:
        RecommendArticleId.extend(Analysis.SQLconfig.sql1.select('dcweb_article_tag', ['article_id'],
                                                        'tag_id = %d' % (i)))
        for ii in RecommendArticleId:
            while RecommendArticleId.count(ii) > 1:
                RecommendArticleId.remove(ii)
        for iii in ReadHistory:
            while RecommendArticleId.count(iii[0]) > 0:
                RecommendArticleId.remove(iii[0])
        if len(RecommendArticleId) > numRecommend:
            break
    Analysis.SQLconfig.sql1.delete('dcweb_recommend', 'user_id = %d' % (UserID))
    for i in range(numRecommend):
        if len(RecommendArticleId) > i:
            Analysis.SQLconfig.sql1.add('dcweb_recommend', {'article_id': RecommendArticleId[i],
                                                      'user_id': UserID, 'recommend_id': i+1})
    print "用户%d阅读了："
    for i in ReadHistory:
        print Analysis.SQLconfig.sql1.select('dcweb_article', ['title'], 'id = %d' % (i[0]))[0].decode('utf8')
    print "智能推荐文章标题："
    for i in RecommendArticleId:
        print Analysis.SQLconfig.sql1.select('dcweb_article', ['title'], 'id = %d' % (i))[0].decode('utf8')

