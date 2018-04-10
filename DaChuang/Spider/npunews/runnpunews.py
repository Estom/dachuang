# -*- coding:utf-8 -*-


import os
import logging

def RunNpunewsSpider():

    logging.basicConfig(filename='runnpunews.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


    # 查看当前工作目录
    retval = os.getcwd()
    print "当前工作目录为 %s" % retval

    os.chdir('./Spider/npunews')

    retval = os.getcwd()
    print "目录修改成功 %s" % retval

    try:
        os.system("scrapy crawl gdyw")  # 工大要闻
    except Exception, e:
        logging.debug('工大要闻')

    try:
        os.system("scrapy crawl xyxw")  # 校园动态
    except Exception, e:
        logging.debug('校园动态')

    try:
        os.system("scrapy crawl PartyCommittee")
    except Exception, e:
        logging.debug('党委宣传部')

if __name__ == "__main__":
    RunNpunewsSpider()



