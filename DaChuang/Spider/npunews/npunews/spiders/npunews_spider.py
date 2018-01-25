#!/usr/bin/python
# -*- coding:utf-8 -*-

# from scrapy.contrib.spiders import  CrawlSpider,Rule

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from npunews.items import NpunewsItem
from urlparse import urljoin

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import re

class NpuNewsSpider(Spider):
    """工大新闻网-工大要闻爬虫"""

    name = "npunews"
    custom_settings = {
        'ITEM_PIPELINES': {'npunews.pipelines.MySQLNpunewsPipeline': 300,},
    }

    #减慢爬取速度
    download_delay = 3 #1

    allowed_domains = ["nwpu.edu.cn"]
    start_urls = [
        "http://news.nwpu.edu.cn/news/gdyw/333.htm", #333
        # "http://news.nwpu.edu.cn/news/gdyw.htm",
        # "http://news.nwpu.edu.cn/news/xyxw.htm",
        "http://news.nwpu.edu.cn/news/xyxw/415.htm" #415
    ]

    # 收集处理一部分数据
    def parse(self, response):
        #items = []
        """
        获取source:工大要闻
        """
        data_source = response.xpath('//table[@class="winstyle48018"]')
        if len(data_source.extract()) <= 0:
            item_source = "No source"
        else:
            str_source = data_source.xpath('string(.)').extract()[0]
            item_source = str_source[len(str_source) - 4: len(str_source)]  # 切片



        for i in range(10,32):# 左闭右开区间
            data = response.xpath('//tr[@id="''line48019_'+ str(i) + '"]')

            for sel in data:
                item = NpunewsItem()

                item['source'] = item_source

                # 提取标题
                # if len(sel.xpath('./td/a/text()').extract()) <= 0:
                if len(sel.xpath('./td[@style="font-size:9pt"]/a/text()').extract()) <= 0:
                    item['title'] = 'No title'
                else:
                    item['title'] = sel.xpath('./td/a/text()').extract()[0].encode('utf-8')


                # 提取发布时间
                if len(sel.xpath('./td[@width="1%"]/span/text()').extract()) <= 0:
                    item['posttime'] = 'No posttime'
                else:
                    item['posttime'] = sel.xpath('./td[@width="1%"]/span/text()').extract()[0].encode('utf-8')

                # 提取url
                if len(sel.xpath('./td/a/@href').extract()) <= 0:
                    item['url'] = 'No url'
                else:
                    temp_url = sel.xpath('./td/a/@href').extract()[0].encode('utf-8')
                    # print temp_url
                    value = re.match(r'../../info/', temp_url)
                    # print value
                    if value:
                        item['url'] = urljoin("http://news.nwpu.edu.cn/info/1002/51024.htm", temp_url)
                    else:
                        item['url'] = urljoin("http://news.nwpu.edu.cn/info/", temp_url)
                        # print 5


                    # 进一步爬取内容

                    yield Request(item['url'], meta={'item':item},callback=self.parse_content)


        # 获取上一页的url
        prev_url = response.xpath('//div/a[2]/@href')
        if len(prev_url.extract()) <= 0:
            pass
        else:
            temp_starturls_prev = prev_url.extract()[0].encode('utf-8')
            temp_searchurl = item['url']
            value = re.search(r'1002', temp_searchurl)
            if value:
                starturls_prev = urljoin("http://news.nwpu.edu.cn/news/gdyw/", temp_starturls_prev)
            else:
                starturls_prev = urljoin("http://news.nwpu.edu.cn/news/xyxw/", temp_starturls_prev)

            yield Request(starturls_prev, callback=self.parse)


    """
    进一步爬取内容content
    """
    def parse_content(self,response):

        item = response.meta['item']

        data = response.xpath('//div[@id="vsb_content_2"]')
        item['content'] = data[0].xpath('string(.)').extract()[0]

        data1 = response.xpath('//span[@class="c52366_author"]')
        strauthor = data1[0].xpath('string(.)').extract()[0]
        item['author'] = strauthor[0 : len(strauthor)-6] #切片

        yield item