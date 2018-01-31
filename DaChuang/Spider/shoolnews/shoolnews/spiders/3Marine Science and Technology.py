# -*- coding: utf-8 -*-

'''
航海 Marine Science and Technology 海洋科技
'''

import scrapy
import sys
import os
import re
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin


class MarineScienceSpider(scrapy.Spider):
    name = 'MarineScience'
    allowed_domains = ['hanghai.nwpu.edu.cn']
    start_urls = [
        # 'http://hanghai.nwpu.edu.cn/index/xyxw.htm',
        'http://hanghai.nwpu.edu.cn/index/xyxw/83.htm',
        'http://hanghai.nwpu.edu.cn/index/xyxw/82.htm',
        'http://hanghai.nwpu.edu.cn/index/xyxw/81.htm',
        'http://hanghai.nwpu.edu.cn/index/xyxw/80.htm'
        ]

    base_image_html = 'http://hanghai.nwpu.edu.cn'

    base_path = 'C:/Images/' + '航海学院'

    if not os.path.exists(base_path.decode('utf-8')):
        os.makedirs(base_path.decode('utf-8'))


    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        print 'parse....'

        # for i in range(0, 10):  # 左闭右开区间
        for i in range(3, 13):  # 左闭右开区间
            data = response.xpath('//tr[@id="''line193647_' + str(i) + '"]')

            for tr in data:
                item = ShoolnewsItem()

                item['author'] = '航海学院'

                # 发布时间
                if len(tr.xpath('./td[3]/span/text()').extract()):
                    item['posttime'] = tr.xpath('./td[3]/span/text()').extract()[0].strip().encode('utf-8')

                    print 'posttime : ', item['posttime']

                # 文章标题 文章网址
                if len(tr.xpath('./td[2]/a/text()').extract()):
                    data = tr.xpath('./td[2]/a')
                    title = data[0].xpath('string(.)').extract()[0].strip().encode('utf-8')
                    item['title'] = title

                    temp_url = tr.xpath('./td[2]/a/@href').extract()[0].encode('utf-8')
                    value = re.search(r'../../info/', temp_url)
                    # print value
                    if value:
                        item['url'] = urljoin("http://hanghai.nwpu.edu.cn/info/1002/51024.htm", temp_url)
                    else:
                        item['url'] = urljoin("http://hanghai.nwpu.edu.cn/info/", temp_url)


                    print 'title : ', item['title']
                    print 'url : ', item['url']

                    yield scrapy.Request(item['url'], meta=item, dont_filter=True,
                         headers=self.settings.get('DEFAULT_REQUEST_HEADERS'), callback=self.parse_content)


    def parse_content(self, response):

        item = response.meta

        print "parse_content...", item['url']

        # 图片网址 图片地址
        if len(response.xpath('//img[@class="img_vsb_content"]/@src').extract()):
            item['image_path'] = self.base_path + '/' + item['title'] + '.jpg'
            item['image_html'] = self.base_image_html + response.xpath('//img[@class="img_vsb_content"]/@src').extract()[0].encode('utf-8')

        elif len(response.xpath('//div[@class="v_news_content"]//img/@src').extract()):
            item['image_path'] = self.base_path + '/' + item['title'] + '.jpg'
            item['image_html'] = self.base_image_html + response.xpath('//div[@class="v_news_content"]//img/@src').extract()[0].encode('utf-8')

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


