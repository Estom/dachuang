# -*- coding: utf-8 -*-

'''
理学院 school of Natural and Applied Sciences
'''

import scrapy
import sys
import re
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin

import datetime
import Myfilter
import time
import hashlib


class NaturalandAppliedSciencesSpider(scrapy.Spider):
    name = 'NaturalandAppliedSciences'
    allowed_domains = ['lxy.nwpu.edu.cn']

    start_urls = [
        # 'http://lxy.nwpu.edu.cn/new/index/xwkx/2.htm',


        # 'http://lxy.nwpu.edu.cn/new/index/xwkx/81.htm',
        # 'http://lxy.nwpu.edu.cn/new/index/xwkx/82.htm',
        # 'http://lxy.nwpu.edu.cn/new/index/xwkx/83.htm',
        'http://lxy.nwpu.edu.cn/new/index/xwkx.htm'
    ]

    base_image_html = 'http://lxy.nwpu.edu.cn'

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        print 'parse....'
        myfilter = Myfilter.MyFilter()
        lasttime = myfilter.FilterbyTime('理学院')

        print 'lasttime: ', lasttime
        if lasttime:
            timeslist = []
            list = response.xpath('//ul[@class="new-ul"]/li')

            for tr in list:  # 左闭右开区间
                item = ShoolnewsItem()

                item['author'] = '理学院'

                # 发布时间
                if len(tr.xpath('./div').extract()):
                    h1 = tr.xpath('./div/h3/text()').extract()[0].encode(
                        'utf-8')  # 日
                    p = tr.xpath('./div/p/text()').extract()[0].encode(
                        'utf-8')  # 年.月
                    item['posttime'] = p + '-' + h1  # 形如 2017-8-7

                    item['posttime'] = datetime.datetime.strptime(
                        item['posttime'].replace(".", "-"), '%Y-%m-%d')
                    print 'posttimetype: ', type(item['posttime'])
                    print 'posttime : ', item['posttime']

                    # 时间字符串也可以直接比大小
                    if item['posttime'] > lasttime:
                        timeslist.append(item['posttime'])

                        # 文章标题 文章网址
                        if len(tr.xpath('./div//a/text()').extract()):
                            data = tr.xpath('./div//a')
                            title = data[0].xpath('string(.)').extract()[0].strip().encode(
                                'utf-8')
                            item['title'] = title

                            temp_url = tr.xpath('./div//a/@href').extract()[0].encode(
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
                                    "http://lxy.nwpu.edu.cn/info/1002/51024.htm",
                                    temp_url)
                                print 'title : ', item['title']
                                print 'url : ', item['url']

                                yield scrapy.Request(item['url'], meta=item,
                                                     dont_filter=True,
                                                     headers=self.settings.get(
                                                         'DEFAULT_REQUEST_HEADERS'),
                                                     callback=self.parse_content)
                    else:
                        print '时间爬过了'

            # 循环结束后更新数据表里的时间
            if timeslist:
                latesttime = max(timeslist)
                myfilter.SaveLatestTime(latesttime, '理学院')

        else:
            print '数据库中没有lasttime'




    def parse_content(self, response):

        item = response.meta

        print "parse_content...", item['url']

        # 图片网址 图片地址
        if len(response.xpath(
                '//img[@class="img_vsb_content"]/@src').extract()):
            item['image_path'] = 'art/' + self.name + hashlib.md5(
                str(time.clock()).encode('utf-8')).hexdigest() + '.jpg'
            item['image_html'] = self.base_image_html + response.xpath(
                '//img[@class="img_vsb_content"]/@src').extract()[0].encode(
                'utf-8')

        elif len(response.xpath(
                '//div[@class="v_news_content"]//img/@src').extract()):
            item['image_path'] = 'art/' + self.name + hashlib.md5(
                str(time.clock()).encode('utf-8')).hexdigest() + '.jpg'
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