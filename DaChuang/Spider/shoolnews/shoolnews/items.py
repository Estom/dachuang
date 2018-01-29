# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#可以使用同一个Item内容，只有spider的内容不同。
class ShoolnewsItem(scrapy.Item):
    # define the fields for your item here like:

    title = scrapy.Field() #
    author = scrapy.Field() #
    content = scrapy.Field() #
    image_path = scrapy.Field() #
    image_html = scrapy.Field() #
    posttime = scrapy.Field() #
    url = scrapy.Field() #
    # source_id = scrapy.Field()



