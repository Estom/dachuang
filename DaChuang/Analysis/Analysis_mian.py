#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import AutoDesc.auto_abstract
import Classify.Classification
import TagCloud.gethotword
import TagCloud.matchWordAndContent
import TransPath.TransPath

def RunAnalysis():
    logging.basicConfig(filename='Analysislog.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    print "文本处理开始："
    try:
        print "分类开始\n"
        Classify.Classification.RunClassify()
        print "分类结束\n"
    except Exception, e:
        logging.debug("分类算法出错")

    try:
        print "摘要开始"
        AutoDesc.auto_abstract.RunAbstract()
        print "摘要结束"
    except Exception, e:
        logging.debug("自动摘要出错")

    try:
        print "文章转移开始"
        TransPath.TransPath.runTransPath()
    except Exception, e:
        logging.debug("转移路径出错")

    try:
        print "关键词统计开始"
        TagCloud.gethotword.rungethotword()
        try:
            TagCloud.matchWordAndContent.runmatchWordAndContent()
        except Exception, e:
            logging.debug("热词与文章匹配发生错误")
    except Exception, e:
        logging.debug("统计热词发生错误")

if __name__ == '__main__':
    RunAnalysis()
