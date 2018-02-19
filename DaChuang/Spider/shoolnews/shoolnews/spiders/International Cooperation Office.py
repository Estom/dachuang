# -*- coding: utf-8 -*-

"""
国际合作处  International Cooperation Office
"""

import scrapy
import sys
import os
import datetime
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin

import datetime
import Myfilter

class InternationalCooperationOfficeSpider(scrapy.Spider) :
    name = 'InternationalCooperationOffice'
    allowed_domains = ['guoji.nwpu.edu.cn']
    start_urls = [
        'http://guoji.nwpu.edu.cn/axshx/lxfc1.htm',
    ]

    base_article_html = "http://guoji.nwpu.edu.cn/info/"
    base_image_html = 'http://guoji.nwpu.edu.cn'

    base_path = 'C:/Images/' + '国际合作处'

    if not os.path.exists(base_path.decode('utf-8')):
        os.makedirs(base_path.decode('utf-8'))


    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        list = response.xpath('//div[@class="col-lg-4 col-md-6 col-sm-6 col-xs-12"]\
                              /div[@class="thumbnail"]')

        for tr in list :
            item = ShoolnewsItem()

            item['author'] = '国际合作处'


            # 图片网址
            if len(tr.xpath('./a/img/@src').extract()) :
                item['image_html'] = self.base_image_html + tr.xpath('./a/img/@src').extract()[0].encode('utf-8')
            else:
                item['image_html'] = ''
            print 'image_html : ', item['image_html']

            # 文章网址
            if len(tr.xpath('./a/@href').extract()) :
                tempurl = tr.xpath('./a/@href').extract()[0].encode('utf-8')
                item['url'] = urljoin(self.base_article_html, tempurl)

                print 'url : ', item['url']

                yield scrapy.Request(item['url'], meta=item, dont_filter=True, headers=self.settings.get('DEFAULT_REQUEST_HEADERS'), callback=self.parse_content)


    def parse_content(self, response) :
        print "parse_content"
        item = response.meta

        # 文章标题
        if len(response.xpath('//div[@class="page-header"]/h3/text()').extract()):
            item['title'] = response.xpath('//div[@class="page-header"]/h3/text()').extract()[
                0].encode('utf-8')
            item['image_path'] = self.base_path + '/' + item['title'] + '.jpg'
            print 'title : ', item['title']
            print 'image_path : ', item['image_path']


        # 发布时间
        if len(response.xpath('//div[@class="page-header"]//small/text()').extract()):
            date = response.xpath('//div[@class="page-header"]//small/text()').extract()[0].encode(
                'utf-8')
            item['posttime'] = date[:10]

            print 'posttime : ', item['posttime']


        # 内容
        content = ''
        data = response.xpath('//div[@class="v_news_content"]')
        plist = data[0].xpath('string(.)').extract()[0].strip().encode('utf-8')
        for p in plist.splitlines():
            p = p.strip()  # 去掉每行头尾空白
            if not len(p) :
                continue
            p = p + '\n'
            content += p

        item['content'] = content



        return item
