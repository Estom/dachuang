#! /usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import AutoDesc.auto_abstract
import Classify.Classification
import TagCloud.gethotword
import TagCloud.matchWordAndContent
import TransPath.TransPath

def RunAnalysis():
    logging.basicConfig(filename='Mainlog.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    try:
        Classify.Classification.runClassification()
    except Exception, e:
        logging.debug("分类算法出错")

    try:
        AutoDesc.auto_abstract.runAbstract()
    except Exception, e:
        logging.debug("自动摘要出错")

    try:
        TransPath.TransPath.runTransPath()
    except Exception, e:
        logging.debug("转移路径出错")

    try:
        TagCloud.gethotword.rungethotword()
        try:
            TagCloud.matchWordAndContent.runmatchWordAndContent()
        except Exception, e:
            logging.debug("热词与文章匹配发生错误")
    except Exception, e:
        logging.debug("统计热词发生错误")



