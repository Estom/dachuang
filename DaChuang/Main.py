# -*- coding: utf-8 -*-

import logging
import Spider.npunews.runnpunews
import Spider.shoolnews.runshoolnews
import Spider.wechat.runwechat
import Analysis.Analysis_mian

def RunMain():
    logging.basicConfig(filename='Mainlog.log',level=logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    try:
        Spider.npunews.runnpunews.RunNpunewsSpider()
        logging.info('新闻网爬虫successful')

    except Exception, e:
        logging.debug('新闻网爬虫error')

    try:
        Spider.shoolnews.runshoolnews.RunSchoolnewsSpider()
        logging.info('学院爬虫successful')

    except Exception, e:
        logging.debug('学院爬虫error')

    try:
        Spider.wechat.runwechat.RunWechatSpider()
        logging.info('微信爬虫successful')

    except Exception, e:
        logging.debug('微信爬虫error')

    try:
        Analysis.Analysis_mian.RunAnalysis()
        logging.info('数据分析successful')
    except Exception, e:
        logging.debug('数据分析error')


if __name__ == "__main__":
    print u'执行自动化脚本'
    logging.info('执行自动化脚本')
    RunMain()

