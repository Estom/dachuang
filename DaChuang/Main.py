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
    except Exception, e:
        logging.debug('新闻网爬虫')

    try:
        Spider.shoolnews.runshoolnews.RunSchoolnewsSpider()
    except Exception, e:
        logging.debug('学院爬虫')

    try:
        Spider.wechat.runwechat.RunWechatSpider()
    except Exception, e:
        logging.debug('微信爬虫')

    try:
        Analysis.Analysis_mian.RunAnalysis()
    except Exception, e:
        logging.debug('数据分析')


if __name__ == "__main__":
    RunMain()