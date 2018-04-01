# encoding=utf-8
"""
脚本名称：Analysis_mian.py
脚本作用：数据处理主函数
备注：一键式增量处理，顺序为自动分类，文章摘要，热词统计
"""
import sys
import FormatData
import SQLconfig
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.insert(0, '.\Classify')
sys.path.insert(0, '.\AutoDesc')
sys.path.insert(0, '.\TransPath')
sys.path.insert(0, '.\TagCloud')

print "\n\r--------------开始分类----------------------\n\r"
import Classification   # 分类
print "\n\r--------------分类结束----------------------\n\r"

print "\n\r--------------开始摘要----------------------\n\r"
import auto_abstract    # 自动摘要
print "\n\r--------------摘要结束----------------------\n\r"

print "\n\r--------------开始搬运数据------------------\n\r"
import TransPath        # 搬运数据
print "\n\r--------------搬运数据结束------------------\n\r"

print "\n\r--------------统计热词开始------------------\n\r"
import gethotword       # 统计热词
print "\n\r--------------统计热词结束------------------\n\r"

print "\n\r--------------热词与文章匹配开始-------------\n\r"
import matchWordAndContent  # 热词与文章匹配
print "\n\r--------------热词与文章匹配结束-------------\n\r"

print "\n\r--------------统计数据结束，欢迎再次使用------\n\r"



