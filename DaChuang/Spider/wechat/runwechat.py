# -*- coding: utf-8 -*-

import os

import logging



def RunWechatSpider():
    logging.basicConfig(filename='runwechat.log', level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 查看当前工作目录
    retval = os.getcwd()
    print "当前工作目录为 %s" % retval

    os.chdir('./Spider/wechat')

    retval = os.getcwd()
    print "目录修改成功 %s" % retval

    try:
        os.system("scrapy crawl contentspider")
        logging.info('微信')
    except Exception, e:
        logging.debug('微信')


    # 查看当前工作目录
    retval = os.getcwd()
    print "***** wechat爬虫结束，当前工作目录为 %s" % retval

    os.chdir('../../')

    retval = os.getcwd()
    print "***** wechat爬虫结束，目录修改成功 %s" % retval


if __name__ == "__main__":
    RunWechatSpider()