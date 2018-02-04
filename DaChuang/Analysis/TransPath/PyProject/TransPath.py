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

a = SQLconfig.sql0._getCount('article')
for i in range(a):
    info = SQLconfig.sql0.select('article', ['title', 'content', 'posttime', 'image_path'], None, 1, i)
    dicDate = {'title': info[0], 'content': info[1], 'date_publish': info[2], 'love_count': 0, 'click_count': 0, 'img': info[3]}
    SQLconfig.sql1.add('dcweb_article', dicDate)
    print i
