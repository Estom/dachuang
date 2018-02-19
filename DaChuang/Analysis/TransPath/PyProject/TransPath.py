#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@脚本名称：TransPath.py
@脚本作用：搬运数据
@备注：只搬运了'title'、'content'、'data_publish'、'love_count'=0、'click_count'=0、'img'字段
"""
import SQLconfig
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

i = -1
while True:
    i += 1
    info = SQLconfig.sql0.select('article', ['title', 'author', 'article.desc', 'content', 'image_path', 'posttime',
                                             'category'], None, 1, i)
    if len(info) == 0:
        break
    dicDate = {'title': info[0], 'dcweb_article.desc': info[2], 'content': info[3], 'love_count': 0, 'click_count': 0,
               'date_publish': info[5], 'category_id': info[6], 'publisher_id': SQLconfig.dicPublisher.get(info[1]),
               'img': info[4], }
    SQLconfig.sql1.add('dcweb_article', dicDate)
    print i
