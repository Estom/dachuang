# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapywechatItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    desc = scrapy.Field()
    content = scrapy.Field()
    image_path = scrapy.Field()
    posttime = scrapy.Field()
    url = scrapy.Field()
    source_id= scrapy.Field()