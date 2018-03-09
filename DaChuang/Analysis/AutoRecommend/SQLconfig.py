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
    db='dcserver',
    charset='utf8'
)

# sql1是已处理数据的数据库
sql1 = MySQLTools(
    # host='111.230.181.121',
    host='localhost',
    port=3306,
    user='root',
    # passwd='ykl123',
    passwd='root',
    # db='dcserver',
    db='dcspider',
    charset='utf8'
)

# 推荐的用户id
user_id = 1
