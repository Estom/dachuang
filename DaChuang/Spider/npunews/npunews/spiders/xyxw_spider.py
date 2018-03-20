#!/usr/bin/python
# -*- coding:utf-8 -*-

import scrapy
from npunews.items import NpunewsItem
from urlparse import urljoin
import re
import sys

import datetime
import Myfilter
import time
import hashlib
reload(sys)
sys.setdefaultencoding('utf-8')


class XyxwSpider(scrapy.Spider):
    name = "xyxw"
    allowed_domains = ["news.nwpu.edu.cn"]
    start_urls = [
        'http://news.nwpu.edu.cn/news/xyxw/456.htm',
        'http://news.nwpu.edu.cn/news/xyxw/457.htm',
        'http://news.nwpu.edu.cn/news/xyxw/458.htm',
        'http://news.nwpu.edu.cn/news/xyxw.htm', # 校园动态
    ]

    base_image_html = 'http://news.nwpu.edu.cn'

    # 收集处理一部分数据
    def parse(self, response):
        print '开始parse....'

        myfilter = Myfilter.MyFilter()
        lasttime = myfilter.FilterbyTime('校园动态')

        print 'lasttime: ', lasttime
        if lasttime:
            timeslist = []

            for i in range(0, 20):  # 左闭右开区间
                data = response.xpath('//tr[@id="''line48019_'+ str(i) + '"]')

                for sel in data:
                    item = NpunewsItem()

                    item['author'] = '校园动态'

                    # 提取发布时间
                    if len(sel.xpath('./td[@width="1%"]/span/text()').extract()) :
                        item['posttime'] = sel.xpath('./td[@width="1%"]/span/text()').extract()[0].strip().encode('utf-8')

                        item['posttime'] = datetime.datetime.strptime(
                            item['posttime'].replace("/", "-"), '%Y-%m-%d')
                        print 'posttimetype: ', type(item['posttime'])
                        print 'posttime : ', item['posttime']

                        # 时间字符串也可以直接比大小
                        if item['posttime'] > lasttime:
                            timeslist.append(item['posttime'])

                            # 提取标题
                            if len(sel.xpath('./td[@style="font-size:9pt"]/a/text()').extract()) :
                                item['title'] = sel.xpath('./td/a/text()').extract()[0].strip().encode('utf-8')
                                print 'title : ', item['title']

                            # 提取url
                            if len(sel.xpath('./td/a/@href').extract()) :
                                temp_url = sel.xpath('./td/a/@href').extract()[0].encode('utf-8')

                                value = re.search(r'../../info/', temp_url)
                                if value:
                                    item['url'] = urljoin("http://news.nwpu.edu.cn/info/1002/51024.htm", temp_url)
                                else:
                                    item['url'] = urljoin("http://news.nwpu.edu.cn/info/", temp_url)
                                print 'url : ', item['url']
                                print 'author : ', item['author']

                                # 进一步爬取内容
                                yield scrapy.Request(item['url'], meta={'item':item},callback=self.parse_content)
                        else:
                            print '时间爬过了'

            # 循环结束后更新数据表里的时间
            if timeslist:
                latesttime = max(timeslist)
                myfilter.SaveLatestTime(latesttime, '校园动态')

        else:
            print '数据库中没有lasttime'




    """
    进一步爬取内容content
    """
    def parse_content(self,response):

        item = response.meta['item']

        print "开始parse_content...", item['url']

        # 图片网址 图片地址
        if len(response.xpath('//img[@class="img_vsb_content"]/@src').extract()):
            item['image_path'] = 'art/' + self.name + hashlib.md5(
                str(time.clock()).encode('utf-8')).hexdigest() + '.jpg'
            item['image_html'] = self.base_image_html + \
                                 response.xpath('//img[@class="img_vsb_content"]/@src').extract()[0].encode('utf-8')

        elif len(response.xpath('//div[@class="v_news_content"]//img/@src').extract()):
            item['image_path'] = 'art/' + self.name + hashlib.md5(
                str(time.clock()).encode('utf-8')).hexdigest() + '.jpg'
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

