# encoding=utf-8
"""
脚本名称：Analysis_mian.py
脚本作用：数据处理主函数
备注：一键式增量处理，顺序为自动分类，文章摘要，热词统计
"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.insert(0, '.\Classify')
sys.path.insert(0, '.\AutoDesc')
sys.path.insert(0, '.\TransPath')
sys.path.insert(0, '.\TagCloud')
import Classification   # 分类
import auto_abstract    # 自动摘要
import TransPath        # 搬运数据
import gethotword       # 统计热词
import matchWordAndContent  # 热词与文章匹配

