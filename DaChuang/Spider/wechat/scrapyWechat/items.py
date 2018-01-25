# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapywechatItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    abstract = scrapy.Field()
    author = scrapy.Field()
    content_url = scrapy.Field()
    cover = scrapy.Field()
    datetime = scrapy.Field()
    title = scrapy.Field()
    content_real = scrapy.Field()
    body_html = scrapy.Field()
