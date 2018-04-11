#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import Spider.npunews.runnpunews
import Spider.shoolnews.runshoolnews
import Spider.wechat.runwechat
import Analysis.Analysis_mian

def RunMain():
    logging.basicConfig(filename='Mainlog.log',level=logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    try:
        Spider.npunews.runnpunews.RunNpunewsSpider()
        logging.debug('新闻网爬虫successful')

    except Exception, e:
        logging.debug('新闻网爬虫error')

    try:
        Spider.shoolnews.runshoolnews.RunSchoolnewsSpider()
        logging.debug('学院爬虫successful')

    except Exception, e:
        logging.debug('学院爬虫error')

    try:
        Spider.wechat.runwechat.RunWechatSpider()
        logging.debug('微信爬虫successful')

    except Exception, e:
        logging.debug('微信爬虫error')

    try:
        Analysis.Analysis_mian.RunAnalysis()
        logging.debug('数据分析successful')

    except Exception, e:
        logging.debug('数据分析error')


if __name__ == "__main__":
    RunMain()