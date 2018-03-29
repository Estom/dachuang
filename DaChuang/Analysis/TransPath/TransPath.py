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
    state = SQLconfig.sql0.select('article', ['process_state', 'id'], None, 1, i)
    if len(state) == 0:
        break
    if (state[0] % 2**3)/(2**2) % 2 == 1:
        print "id = %d文章已转移" % state[1]
        continue
    else:
        info = SQLconfig.sql0.select('article', ['title', 'author', 'article.desc', 'content', 'image_path', 'posttime',
                                             'category'], None, 1, i)
        if info[2] is None:
            info[2] = " "
        elif len(info[2]) > 299:
                info[2] = info[2][0:299]
        dicDate = {'title': info[0], 'dcweb_article.desc': info[2], 'content': info[3], 'love_count': 0, 'click_count': 0,
                   'date_publish': info[5], 'category_id': info[6], 'publisher_id': SQLconfig.dicPublisher.get(info[1]),
                   'img': info[4], 'tag_mark': 0}
        SQLconfig.sql1.add('dcweb_article', dicDate)
        SQLconfig.sql0.update('article', {'process_state': state[0] % 2**3 + 2**2}, 'id = %d' % state[1])
        print "转移第id = %d条" % state[1]
