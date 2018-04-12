# -*- coding:utf-8 -*-


import os
import logging

def RunNpunewsSpider():

    logging.basicConfig(filename='runnpunews.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    # 查看当前工作目录
    retval = os.getcwd()
    print "当前工作目录为 %s" % retval

    os.chdir('./Spider/npunews')

    retval = os.getcwd()
    print "目录修改成功 %s" % retval

    try:
        os.system("scrapy crawl gdyw")  # 工大要闻
        logging.info('工大要闻')
    except Exception, e:
        logging.debug('工大要闻')

    try:
        os.system("scrapy crawl xyxw")  # 校园动态
        logging.info('校园动态ac')
    except Exception, e:
        logging.debug('校园动态wa')

    try:
        os.system("scrapy crawl PartyCommittee")
        logging.info('党委宣传部ac')
    except Exception, e:
        logging.debug('党委宣传部wa')


    # 查看当前工作目录
    retval = os.getcwd()
    print "***** npu爬虫结束，当前工作目录为 %s" % retval

    os.chdir('../../')

    retval = os.getcwd()
    print "***** npu爬虫结束，目录修改成功 %s" % retval

if __name__ == "__main__":
    RunNpunewsSpider()



