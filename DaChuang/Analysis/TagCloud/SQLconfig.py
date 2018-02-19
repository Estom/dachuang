#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@脚本名称：SQLconfig.py
@脚本作用：所有数据库配置配置
"""
from MySQLTool import MySQLTools

# sql0是未处理数据库
sql0 = MySQLTools(
    host='111.230.181.121',
    port=3306,
    user='root',
    passwd='ykl123',
    db='dcspider',
    charset='utf8'
)

# sql1是已处理数据的数据库
sql1 = MySQLTools(
    host='111.230.181.121',
    port=3306,
    user='root',
    passwd='ykl123',
    db='dcserver',
    charset='utf8'
)

# 类别字典
dicCategory = {u'学科竞赛': 1, u'学术信息': 2, u'工大新闻': 3, u'招聘就业': 7, u'校园活动': 8, u'通知公告': 10, u'考研留学': 11, u'生活娱乐':12}

# 类别前后改变对应字典
dicClassToCategory = {u'学科竞赛': 1, u'科研信息': 2, u'行政信息': 3, u'招生信息': 3, u'招聘就业': 7, u'校园活动': 8, u'升学留学': 11, u'生活娱乐': 12}

# ###################基础常量###################################
wordbag_path = "train_set.dat"
stopword_path = "hlt_stop_words.txt"
classification_path = "classification_NB.dat"
###############################################################
