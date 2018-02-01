#!/usr/bin/python
# -*- coding:utf-8 -*-

import scrapy
from npunews.items import NpunewsItem
from urlparse import urljoin
import os
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class NpuNewsSpider(scrapy.Spider):
    name = "npunews"
    allowed_domains = ["news.nwpu.edu.cn"]
    start_urls = [
        # "http://news.nwpu.edu.cn/news/gdyw/365.htm", #333 工大新闻
        # 'http://news.nwpu.edu.cn/news/gdyw/351.htm'

        # 'http://news.nwpu.edu.cn/news/gdyw.htm', # 工大新闻
        # 'http://news.nwpu.edu.cn/news/xyxw.htm', # 校园动态
        # "http://news.nwpu.edu.cn/news/xyxw/454.htm", #415 校园动态

        "http://news.nwpu.edu.cn/news/xyxw/450.htm",
    ]

    base_image_html = 'http://news.nwpu.edu.cn'
    base_path = 'C:/Images/' + '工大新闻网'

    if not os.path.exists(base_path.decode('utf-8')):
        os.makedirs(base_path.decode('utf-8'))


    # 收集处理一部分数据
    def parse(self, response):
        print '开始parse....'


        for i in range(3,23):# 左闭右开区间
        # for i in range(0, 20):  # 左闭右开区间
            data = response.xpath('//tr[@id="''line48019_'+ str(i) + '"]')

            for sel in data:
                item = NpunewsItem()

                # 提取标题
                if len(sel.xpath('./td[@style="font-size:9pt"]/a/text()').extract()) :
                    item['title'] = sel.xpath('./td/a/text()').extract()[0].strip().encode('utf-8')
                    print 'title : ', item['title']

                # 提取发布时间
                if len(sel.xpath('./td[@width="1%"]/span/text()').extract()) :
                    item['posttime'] = sel.xpath('./td[@width="1%"]/span/text()').extract()[0].strip().encode('utf-8')
                    print 'posttime : ', item['posttime']

                # 提取url
                if len(sel.xpath('./td/a/@href').extract()) :
                    temp_url = sel.xpath('./td/a/@href').extract()[0].encode('utf-8')

                    value2 = re.search(r'1002', temp_url)
                    if value2:
                        item['author'] = '工大要闻'
                    value3 = re.search(r'1003', temp_url)
                    if value3:
                        item['author'] = '校园动态'

                    value = re.search(r'../../info/', temp_url)
                    if value:
                        item['url'] = urljoin("http://news.nwpu.edu.cn/info/1002/51024.htm", temp_url)
                    else:
                        item['url'] = urljoin("http://news.nwpu.edu.cn/info/", temp_url)
                    print 'url : ', item['url']
                    print 'author : ', item['author']

                    # 进一步爬取内容
                    yield scrapy.Request(item['url'], meta={'item':item},callback=self.parse_content)


        print '结束parse....'


    """
    进一步爬取内容content
    """
    def parse_content(self,response):

        item = response.meta['item']

        print "开始parse_content...", item['url']

        # 图片网址 图片地址
        if len(response.xpath('//img[@class="img_vsb_content"]/@src').extract()):
            item['image_path'] = self.base_path + '/' + item['title'] + '.jpg'
            item['image_html'] = self.base_image_html + \
                                 response.xpath('//img[@class="img_vsb_content"]/@src').extract()[0].encode('utf-8')

        elif len(response.xpath('//div[@class="v_news_content"]//img/@src').extract()):
            item['image_path'] = self.base_path + '/' + item['title'] + '.jpg'
            item['image_html'] = self.base_image_html + \
                                 response.xpath('//div[@class="v_news_content"]//img/@src').extract()[0].encode('utf-8')

        else:
            item['image_path'] = ''
            item['image_html'] = ''

        print 'image_html : ', item['image_html']
        print 'image_path : ', item['image_path']

        # 内容
        content = ''
        data = response.xpath('//div[@class="v_news_content"]')
        plist = data[0].xpath('string(.)').extract()[0].strip().encode('utf-8')
        for p in plist.splitlines():
            p = p.strip()  # 去掉每行头尾空白
            if not len(p):
                continue
            p = p + '\n'
            content += p

        item['content'] = content

        print '结束parse_content...', item['url']

        return item

