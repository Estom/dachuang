# -*- coding: utf-8 -*-

from scrapy import cmdline

# cmdline.execute("scrapy crawl computer".split()) # 1.28

# cmdline.execute("scrapy crawl automation".split()) # 1.30

# cmdline.execute("scrapy crawl electricity".split()) # 1.31

# cmdline.execute("scrapy crawl management".split()) # 1.31

# cmdline.execute("scrapy crawl aeronautic".split()) # 航空 # 1.31

# cmdline.execute("scrapy crawl astronautics".split()) # 航天 # 1.31

# cmdline.execute("scrapy crawl MarineScience".split()) # 航海 # 1.31



# cmdline.execute("scrapy crawl MechanicalEngineering".split()) # 机电 # 2.1

# cmdline.execute("scrapy crawl Humanities".split()) # 人文与经法学院 # 2.1

# cmdline.execute("scrapy crawl LifeSciences".split()) # 生命学院 # 2.1

# cmdline.execute("scrapy crawl ForeignStudies".split()) # 外国语学院 # 2.1

# cmdline.execute("scrapy crawl InternationalCollege".split()) #国际教育学院 # 2.1



# cmdline.execute("scrapy crawl Software".split()) # 软件学院 # 2.2

# cmdline.execute("scrapy crawl PowerandEnergy".split()) # 动力与能源学院 # 2.2

# cmdline.execute("scrapy crawl NaturalandAppliedSciences".split()) # 理学院 # 2.2



# cmdline.execute("scrapy crawl Administration".split()) # 教务处 # 2.3

# cmdline.execute("scrapy crawl InternationalCooperationOffice".split()) # 国际合作处 # 2.3

# cmdline.execute("scrapy crawl InternationalCooperationOfficeNotice".split()) # 国际合作处通知 # 2.3

cmdline.execute("scrapy crawl Marxism".split()) # 马克思主义学院 # 2.3


# 排版太乱 不想爬
# cmdline.execute("scrapy crawl HonorsCollege".split()) # 教育实验学院
# cmdline.execute("scrapy crawl Architecture".split()) # 力学与土木建筑学院

"""
材料学院的新闻大部分在新闻网的校园动态上发布，个人认为单独爬材料学院没有必要!!!
"""
# cmdline.execute("scrapy crawl MaterialsScience".split()) # 1.31