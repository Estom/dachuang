# -*- coding: utf-8 -*-

import os
import logging

def RunSchoolnewsSpider():

    logging.basicConfig(filename='runshoolnews.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 查看当前工作目录
    retval = os.getcwd()
    print "当前工作目录为 %s" % retval

    os.chdir('./Spider/shoolnews')

    retval = os.getcwd()
    print "目录修改成功 %s" % retval

    try:
        os.system("scrapy crawl aeronautic")  # 航空 2.11 1.31
        logging.info('航空ac')
    except Exception, e:
        logging.debug('航空wa')

    try:
        os.system("scrapy crawl astronautics")  # 航天 2.11 # 1.31
        logging.info('航天ac')
    except Exception, e:
        logging.debug('航天wa')

    try:
        os.system("scrapy crawl MarineScience")  # 航海 # 2.11 1.31
        logging.info('航海ac')
    except Exception, e:
        logging.debug('航海wa')

    try:
        os.system("scrapy crawl MaterialsScience")  # 材料 # 2.11 1.31
        logging.info('材料ac')
    except Exception, e:
        logging.debug('材料wa')

    try:
        os.system("scrapy crawl MechanicalEngineering")  # 机电 # 2.11 2.1
        logging.info('机电ac')
    except Exception, e:
        logging.debug('机电wa')

    try:
        os.system("scrapy crawl PowerandEnergy")  # 动力与能源学院 # 2.11 2.2
        logging.info('动力与能源学院ac')
    except Exception, e:
        logging.debug('动力与能源学院wa')

    try:
        os.system("scrapy crawl electricity")  # 电子信息 2.12 1.31
        logging.info('电子信息ac')
    except Exception, e:
        logging.debug('电子信息wa')

    try:
        os.system("scrapy crawl automation")  # 自动化 2.12 1.30
        logging.info('自动化ac')
    except Exception, e:
        logging.debug('自动化wa')

    try:
        os.system("scrapy crawl computer")  # 计算机 2.11 1.28
        logging.info('计算机ac')
    except Exception, e:
        logging.debug('计算机wa')

    try:
        os.system("scrapy crawl NaturalandAppliedSciences")  # 理学院 # 2.12 2.2
        logging.info('理学院ac')
    except Exception, e:
        logging.debug('理学院wa')

    try:
        os.system("scrapy crawl management")  # 管理 2.12 1.31
        logging.info('管理ac')
    except Exception, e:
        logging.debug('管理wa')

    try:
        os.system("scrapy crawl Humanities")  # 人文与经法学院 # 2.12 2.1
        logging.info('人文与经法学院ac')
    except Exception, e:
        logging.debug('人文与经法学院wa')

    try:
        os.system("scrapy crawl Software")  # 软件学院 # 2.12 2.2
        logging.info('软件学院ac')
    except Exception, e:
        logging.debug('软件学院wa')

    try:
        os.system("scrapy crawl LifeSciences")  # 生命学院 # 2.12 2.1
        logging.info('生命学院ac')
    except Exception, e:
        logging.debug('生命学院wa')

    try:
        os.system("scrapy crawl ForeignStudies")  # 外国语学院 # 2.12 2.1
        logging.info('外国语学院ac')
    except Exception, e:
        logging.debug('外国语学院wa')

    try:
        os.system("scrapy crawl InternationalCollege")  # 国际教育学院 # 2.12 2.1
        logging.info('国际教育学院ac')
    except Exception, e:
        logging.debug('国际教育学院wa')

    try:
        os.system("scrapy crawl Marxism")  # 马克思主义学院 # 2.12 2.3
        logging.info('马克思主义学院ac')
    except Exception, e:
        logging.debug('马克思主义学院wa')

    try:
        os.system("scrapy crawl Administration")  # 教务处 # 2.12 2.3
        logging.info('教务处ac')
    except Exception, e:
        logging.debug('教务处wa')

    try:
        os.system("scrapy crawl InternationalCooperationOfficeNotice")  # 国际合作处通知 # 2.12 2.3
        logging.info('国际合作处通知ac')
    except Exception, e:
        logging.debug('国际合作处通知wa')

    # 查看当前工作目录
    retval = os.getcwd()
    print "***** school爬虫结束，当前工作目录为 %s" % retval

    os.chdir('../../')

    retval = os.getcwd()
    print "***** school爬虫结束，目录修改成功 %s" % retval


if __name__ == "__main__":
    RunSchoolnewsSpider()








"""
留学风采不能以时间来过滤，需要单独爬
"""
# cmdline.execute("scrapy crawl InternationalCooperationOffice".split()) # 国际合作处留学风采 # 2.3



# 排版太乱 不想爬
# cmdline.execute("scrapy crawl HonorsCollege".split()) # 教育实验学院
# cmdline.execute("scrapy crawl Architecture".split()) # 力学与土木建筑学院
