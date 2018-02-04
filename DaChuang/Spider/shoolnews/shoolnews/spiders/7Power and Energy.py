# -*- coding: utf-8 -*-

'''
动力与能源 Power and Energy
'''

import scrapy
import sys
import os
import re
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin

class PowerandEnergySpider(scrapy.Spider):
    name = 'PowerandEnergy'
    allowed_domains = ['dongneng.nwpu.edu.cn']

    start_urls = [
        'http://dongneng.nwpu.edu.cn/newwz/sy/xwdt.htm',
        # 'http://dongneng.nwpu.edu.cn/newwz/sy/xwdt/74.htm',
        # 'http://dongneng.nwpu.edu.cn/newwz/sy/xwdt/73.htm',
    ]

    base_image_html = 'http://dongneng.nwpu.edu.cn'

    base_path = 'C:/Images/' + '动力与能源学院'

    if not os.path.exists(base_path.decode('utf-8')):
        os.makedirs(base_path.decode('utf-8'))

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        print 'parse....'
        list = response.xpath('//div[@class="news-txt-list"]/dl')

        for tr in list:  # 左闭右开区间
            item = ShoolnewsItem()

            item['author'] = '动力与能源学院'

            # 发布时间
            if len(tr.xpath('./dt/div/@class').extract()):
                h1 = tr.xpath('./dt/div/span[1]/text()').extract()[0].encode('utf-8') # 月-日
                p = tr.xpath('./dt/div/span[2]/text()').extract()[0].encode('utf-8') # 年
                date = p + '.' + h1 # 形如 2017-8-7
                item['posttime'] = date

                print 'posttime : ', item['posttime']

            # 文章标题 文章网址
            if len(tr.xpath('./dd//a/text()').extract()):
                data = tr.xpath('./dd//a')
                title = data[0].xpath('string(.)').extract()[0].strip().encode('utf-8')
                item['title'] = title

                temp_url = tr.xpath('./dd//a/@href').extract()[0].encode(
                    'utf-8')

                value2 = re.search(r'http://news.nwpu.', temp_url)
                if value2:
                    pass
                else:
                    value = re.search(r'../../../info/', temp_url)
                    # print value
                    if value:
                        temp_url = temp_url[3:]
                    else:
                        pass

                    item['url'] = urljoin(
                        "http://dongneng.nwpu.edu.cn/info/1002/51024.htm",
                        temp_url)
                    print 'title : ', item['title']
                    print 'url : ', item['url']

                    yield scrapy.Request(item['url'], meta=item,
                                         dont_filter=True,
                                         headers=self.settings.get(
                                             'DEFAULT_REQUEST_HEADERS'),
                                         callback=self.parse_content)

    def parse_content(self, response):

        item = response.meta

        print "parse_content...", item['url']

        # 图片网址 图片地址
        if len(response.xpath(
                '//img[@class="img_vsb_content"]/@src').extract()):
            item['image_path'] = self.base_path + '/' + item['title'] + '.jpg'
            item['image_html'] = self.base_image_html + response.xpath(
                '//img[@class="img_vsb_content"]/@src').extract()[0].encode(
                'utf-8')

        elif len(response.xpath(
                '//div[@class="v_news_content"]//img/@src').extract()):
            item['image_path'] = self.base_path + '/' + item['title'] + '.jpg'
            item['image_html'] = self.base_image_html + response.xpath(
                '//div[@class="v_news_content"]//img/@src').extract()[0].encode(
                'utf-8')

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