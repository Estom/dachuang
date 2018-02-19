# -*- coding: utf-8 -*-

'''
马克思主义学院 school of Marxism
'''

import scrapy
import sys
import os
import re
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin

import datetime
import Myfilter

class MarxismSpider(scrapy.Spider):
    name = 'Marxism'
    allowed_domains = ['marx.nwpu.edu.cn']

    start_urls = [
        'http://marx.nwpu.edu.cn/xwgg/xwdt.htm',
    ]

    base_image_html = 'http://marx.nwpu.edu.cn'

    base_path = 'C:/Images/' + '马克思主义学院'

    if not os.path.exists(base_path.decode('utf-8')):
        os.makedirs(base_path.decode('utf-8'))


    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        print 'parse....'

        myfilter = Myfilter.MyFilter()
        lasttime = myfilter.FilterbyTime('马克思主义学院')

        print 'lasttime: ', lasttime
        if lasttime:
            timeslist = []
            for i in range(0, 20):  # 左闭右开区间
            # for i in range(13, 33):  # 左闭右开区间
                data = response.xpath('//tr[@id="''line60381_' + str(i) + '"]')

                for tr in data:
                    item = ShoolnewsItem()

                    item['author'] = '马克思主义学院'

                    # 发布时间
                    if len(tr.xpath('./td[2]/span/text()').extract()):
                        date = tr.xpath('./td[2]/span/text()').extract()[0].strip().encode('utf-8')
                        item['posttime'] = date[1:11]
                        item['posttime'] = datetime.datetime.strptime(
                            item['posttime'].replace("/", "-"), '%Y-%m-%d')
                        print 'posttimetype: ', type(item['posttime'])
                        print 'posttime : ', item['posttime']

                        # 时间字符串也可以直接比大小
                        if item['posttime'] > lasttime:
                            timeslist.append(item['posttime'])

                            # 文章网址
                            if len(tr.xpath('./td[1]/a/text()').extract()):
                                temp_url = tr.xpath('./td[1]/a/@href').extract()[0].encode('utf-8')

                                value2 = re.search(r'http://news.nwpu.', temp_url)
                                print value2
                                if value2:
                                    pass
                                else :
                                    value = re.search(r'../../info/', temp_url)
                                    # print value
                                    if value:
                                        item['url'] = urljoin("http://marx.nwpu.edu.cn/info/1002/51024.htm", temp_url)
                                    else:
                                        item['url'] = urljoin("http://marx.nwpu.edu.cn/info/", temp_url)

                                    print 'url : ', item['url']

                                    yield scrapy.Request(item['url'], meta=item, dont_filter=True,
                                     headers=self.settings.get('DEFAULT_REQUEST_HEADERS'), callback=self.parse_content)
                        else:
                            print '时间爬过了'

            # 循环结束后更新数据表里的时间
            if timeslist:
                latesttime = max(timeslist)
                myfilter.SaveLatestTime(latesttime, '马克思主义学院')

        else:
            print '数据库中没有lasttime'



    def parse_content(self, response):

        item = response.meta

        print "parse_content...", item['url']

        # 文章标题
        if len(response.xpath('//div[@class="wz_nr"]/h1[@class="w_title"]/text()').extract()):
            item['title'] = response.xpath('//div[@class="wz_nr"]/h1[@class="w_title"]/text()').extract()[0].encode('utf-8')
            print 'title : ', item['title']

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
