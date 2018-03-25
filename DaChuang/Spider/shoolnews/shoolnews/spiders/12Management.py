# -*- coding: utf-8 -*-

'''
管理学院
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


class ManagementSpider(scrapy.Spider):
    name = 'management'
    allowed_domains = ['som.nwpu.edu.cn']
    start_urls = [
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/2.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/3.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/4.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/5.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/6.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/7.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/8.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/9.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/10.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/11.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/12.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/13.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/14.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/15.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/16.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/17.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/18.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/19.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/20.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/21.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/22.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/23.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/24.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/25.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/26.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/27.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/28.htm',

        # 'http://som.nwpu.edu.cn/xxfb/xyxw/29.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/30.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/31.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/32.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/33.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/34.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/35.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/36.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/37.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/38.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/39.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/40.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/41.htm',

        # 'http://som.nwpu.edu.cn/xxfb/xyxw/42.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/43.htm',
        # 'http://som.nwpu.edu.cn/xxfb/xyxw/44.htm',
        'http://som.nwpu.edu.cn/xxfb/xyxw.htm',
    ]

    base_image_html = 'http://som.nwpu.edu.cn'  # 图片的基网址  # /__local/B/E4/8C/5523A744CCF08A289BBE3FCA210_2705AB4A_FE6C.jpg

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        print 'parse....'

        myfilter = Myfilter.MyFilter()
        lasttime = myfilter.FilterbyTime('管理学院')

        print 'lasttime: ', lasttime
        if lasttime:
            timeslist = []
            for i in range(0, 20):  # 左闭右开区间
            # for i in range(1, 21):  # 左闭右开区间
                data = response.xpath('//tr[@id="''line57742_' + str(i) + '"]')

                for tr in data:
                    item = ShoolnewsItem()

                    item['author'] = '管理学院'

                    # 发布时间
                    if len(tr.xpath('./td[3]/span/text()').extract()):
                        item['posttime'] = tr.xpath('./td[3]/span/text()').extract()[0].strip().encode('utf-8')

                        item['posttime'] = datetime.datetime.strptime(
                            item['posttime'].replace("/", "-"), '%Y-%m-%d')
                        print 'posttimetype: ', type(item['posttime'])
                        print 'posttime : ', item['posttime']

                        # 时间字符串也可以直接比大小
                        if item['posttime'] > lasttime:
                            timeslist.append(item['posttime'])

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
                        else:
                            print '时间爬过了'

            # 循环结束后更新数据表里的时间
            if timeslist:
                latesttime = max(timeslist)
                myfilter.SaveLatestTime(latesttime, '管理学院')

        else:
            print '数据库中没有lasttime'



    def parse_content(self, response):

        item = response.meta

        print "parse_content...", item['url']

        # 图片网址 图片地址
        if len(response.xpath('//img[@class="img_vsb_content"]/@src').extract()):
            item['image_path'] = 'art/' + self.name + hashlib.md5(
                str(time.clock()).encode('utf-8')).hexdigest() + '.jpg'
            item['image_html'] = self.base_image_html + response.xpath('//img[@class="img_vsb_content"]/@src').extract()[0].encode('utf-8')

        elif len(response.xpath('//div[@class="v_news_content"]//img/@src').extract()):
            item['image_path'] = 'art/' + self.name + hashlib.md5(
                str(time.clock()).encode('utf-8')).hexdigest() + '.jpg'
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
