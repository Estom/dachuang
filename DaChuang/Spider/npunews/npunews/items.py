# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy

class NpunewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 标题
    url = scrapy.Field()  # 链接
    #desc = scrapy.Field()  # 简述
    content = scrapy.Field(); #内容
    posttime = scrapy.Field()  # 发布时间
    author = scrapy.Field() # 作者
    source = scrapy.Field() # 来源