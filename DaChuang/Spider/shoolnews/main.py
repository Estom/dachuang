# -*- coding: utf-8 -*-

import os

# os.system("scrapy crawl aeronautic") # 航空 2.11 1.31
# os.system("scrapy crawl astronautics") # 航天 2.11 # 1.31
# os.system("scrapy crawl MarineScience") # 航海 # 2.11 1.31
os.system("scrapy crawl MaterialsScience")  # 材料 # 2.11 1.31
os.system("scrapy crawl MechanicalEngineering") # 机电 # 2.11 2.1

# os.system("scrapy crawl PowerandEnergy") # 动力与能源学院 # 2.11 2.2
# os.system("scrapy crawl electricity") # 2.12 1.31
# os.system("scrapy crawl automation") # 2.12 1.30
# # os.system("scrapy crawl computer") # 2.11 1.28
# os.system("scrapy crawl NaturalandAppliedSciences") # 理学院 # 2.12 2.2
# os.system("scrapy crawl management") # 2.12 1.31
# os.system("scrapy crawl Humanities") # 人文与经法学院 # 2.12 2.1
# os.system("scrapy crawl Software") # 软件学院 # 2.12 2.2
# os.system("scrapy crawl LifeSciences") # 生命学院 # 2.12 2.1
# os.system("scrapy crawl ForeignStudies") # 外国语学院 # 2.12 2.1
# # os.system("scrapy crawl InternationalCollege") #国际教育学院 # 2.12 2.1
# os.system("scrapy crawl Marxism") # 马克思主义学院 # 2.12 2.3
# # os.system("scrapy crawl Administration") # 教务处 # 2.12 2.3
# # os.system("scrapy crawl InternationalCooperationOfficeNotice") # 国际合作处通知 # 2.12 2.3



"""
留学风采不能以时间来过滤，需要单独爬
"""
# cmdline.execute("scrapy crawl InternationalCooperationOffice".split()) # 国际合作处留学风采 # 2.3




# 排版太乱 不想爬
# cmdline.execute("scrapy crawl HonorsCollege".split()) # 教育实验学院
# cmdline.execute("scrapy crawl Architecture".split()) # 力学与土木建筑学院
