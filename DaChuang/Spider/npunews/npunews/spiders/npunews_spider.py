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


class GdywSpider(scrapy.Spider):
    name = "gdyw"
    allowed_domains = ["news.nwpu.edu.cn"]
    start_urls = [
        # 'http://news.nwpu.edu.cn/news/gdyw/280.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/281.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/282.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/283.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/284.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/285.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/286.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/287.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/288.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/289.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/290.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/291.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/292.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/293.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/294.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/295.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/296.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/297.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/298.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/299.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/300.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/301.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/302.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/303.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/304.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/305.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/306.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/307.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/308.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/309.htm',

        # 'http://news.nwpu.edu.cn/news/gdyw/310.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/311.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/312.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/313.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/314.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/315.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/316.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/317.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/318.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/319.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/320.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/321.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/322.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/323.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/324.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/325.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/326.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/327.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/328.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/329.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/330.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/331.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/332.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/333.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/334.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/335.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/336.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/337.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/338.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/339.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/340.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/341.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/342.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/343.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/344.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/345.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/346.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/347.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/348.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/349.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/350.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/351.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/352.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/353.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/354.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/355.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/356.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/357.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/358.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/359.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/360.htm',

        # 'http://news.nwpu.edu.cn/news/gdyw/362.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/364.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/367.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/368.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/369.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/370.htm',
        # 'http://news.nwpu.edu.cn/news/gdyw/371.htm',
        'http://news.nwpu.edu.cn/news/gdyw.htm', # 工大要闻
    ]

    base_image_html = 'http://news.nwpu.edu.cn'

    # 收集处理一部分数据
    def parse(self, response):
        print '开始parse....'

        myfilter = Myfilter.MyFilter()
        lasttime = myfilter.FilterbyTime('工大要闻')

        print 'lasttime: ', lasttime
        if lasttime:
            timeslist = []

            for i in range(0, 20):  # 左闭右开区间
                data = response.xpath('//tr[@id="''line48019_'+ str(i) + '"]')

                for sel in data:
                    item = NpunewsItem()

                    item['author'] = '工大要闻'

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
                myfilter.SaveLatestTime(latesttime, '工大要闻')

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

