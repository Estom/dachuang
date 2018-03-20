# -*- coding: utf-8 -*-

'''
自动化 Automation
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

class AutomationSpider(scrapy.Spider):
    name = 'automation'
    allowed_domains = ['zdhxy.nwpu.edu.cn']
    start_urls = [
        'http://zdhxy.nwpu.edu.cn/xwgg/tuxw/49.htm',
        'http://zdhxy.nwpu.edu.cn/xwgg/tuxw/50.htm',
        'http://zdhxy.nwpu.edu.cn/xwgg/tuxw.htm'
    ]

    base_article_html = "http://zdhxy.nwpu.edu.cn/info/"
    base_image_html = 'http://zdhxy.nwpu.edu.cn' # 图片的基网址  # /__local/B/E4/8C/5523A744CCF08A289BBE3FCA210_2705AB4A_FE6C.jpg

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        list = response.xpath('/html/body/div/div[4]/div[3]/table/tr')

        myfilter = Myfilter.MyFilter()
        lasttime = myfilter.FilterbyTime('自动化学院')

        print 'lasttime: ', lasttime
        if lasttime:
            timeslist = []
            for tr in list:
                item = ShoolnewsItem()

                item['author'] = '自动化学院'

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
                            # 排版很坑 标题有时在./td[2]/a一级，有时在./td[2]/a/span一级,改为用string而不是text
                            data = tr.xpath('./td[2]/a')
                            title = data[0].xpath('string(.)').extract()[0].strip().encode('utf-8')
                            item['title'] = title


                            temp_url = tr.xpath('./td[2]/a/@href').extract()[0].encode('utf-8')
                            value = re.search(r'../../info/', temp_url)
                            # print value
                            if value:
                                item['url'] = urljoin("http://zdhxy.nwpu.edu.cn/info/1002/51024.htm", temp_url)
                            else:
                                item['url'] = urljoin("http://zdhxy.nwpu.edu.cn/info/", temp_url)


                            print 'title : ', item['title']
                            print 'url : ', item['url']

                            yield scrapy.Request(item['url'], meta=item, dont_filter=True, headers=self.settings.get('DEFAULT_REQUEST_HEADERS'), callback=self.parse_content)
                    else:
                        print '时间爬过了'

            # 循环结束后更新数据表里的时间
            if timeslist:
                latesttime = max(timeslist)
                myfilter.SaveLatestTime(latesttime, '自动化学院')

        else:
            print '数据库中没有lasttime'


    def parse_content(self, response):

        item = response.meta

        print "parse_content...", item['url']

        # 图片网址 图片地址
        if len(response.xpath('//img[@class="img_vsb_content"]/@src').extract()) :
            item['image_path'] = 'art/' + self.name + hashlib.md5(
                str(time.clock()).encode('utf-8')).hexdigest() + '.jpg'
            item['image_html'] = self.base_image_html + response.xpath('//img[@class="img_vsb_content"]/@src').extract()[0].encode('utf-8')

        elif len(response.xpath('//div[@class="v_news_content"]//img/@src').extract()) :
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