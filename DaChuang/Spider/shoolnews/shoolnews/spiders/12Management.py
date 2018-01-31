# -*- coding: utf-8 -*-

'''
管理学院
'''

import scrapy
import sys
import os
import re
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin


class ManagementSpider(scrapy.Spider):
    name = 'management'
    allowed_domains = ['som.nwpu.edu.cn']
    start_urls = [
                  # 'http://som.nwpu.edu.cn/xxfb/xyxw.htm',
                  # 'http://som.nwpu.edu.cn/xxfb/xyxw/41.htm',
                  'http://som.nwpu.edu.cn/xxfb/xyxw/40.htm'
                  ]

    base_image_html = 'http://som.nwpu.edu.cn'  # 图片的基网址  # /__local/B/E4/8C/5523A744CCF08A289BBE3FCA210_2705AB4A_FE6C.jpg

    base_path = 'C:/Images/' + '管理学院'  # 图片保存到本地的基地址

    # 建立文件夹'C:/Images/管理学院'

    if not os.path.exists(base_path.decode('utf-8')):
        os.makedirs(base_path.decode('utf-8'))


    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        print 'parse....'

        # for i in range(0, 20):  # 左闭右开区间
        for i in range(1, 21):  # 左闭右开区间
            data = response.xpath('//tr[@id="''line57742_' + str(i) + '"]')

            for tr in data:
                item = ShoolnewsItem()

                item['author'] = '管理学院'

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
                        item['url'] = urljoin("http://som.nwpu.edu.cn/info/1002/51024.htm", temp_url)
                    else:
                        item['url'] = urljoin("http://som.nwpu.edu.cn/info/", temp_url)


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
