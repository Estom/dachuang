#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
脚本名称：initTrainDate.py
脚本作用：初始化训练分类数据
"""
import SQLconfig
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
a = SQLconfig.sql1._getCount('train')
for ii in range(a):
    info = SQLconfig.sql1.select('train', ['title', 'content', 'class'], None, 1, ii)
    info[2] = SQLconfig.dicClassToCategory.get(info[2])
    print u'%d: %s, %d\n' % (ii+1, info[0], info[2])
    dicDate = {'title': info[0], 'content': info[1], 'category_id': info[2]}
    SQLconfig.sql0.add('train', dicDate)
