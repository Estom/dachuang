# -*- coding: utf-8 -*-

'''
计算机 Computer Science and Technology
'''

import scrapy
import sys
import datetime
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin

import Myfilter
import time
import hashlib

class ComputerSpider(scrapy.Spider) :
    name = 'computer'
    allowed_domains = ['jsj.nwpu.edu.cn']
    start_urls = [
        'http://jsj.nwpu.edu.cn/new/news.jsp?a197110t=7&a197110p=5&a197110c=10&urltype=tree.TreeTempUrl&wbtreeid=1317',
        'http://jsj.nwpu.edu.cn/new/news.jsp?a197110t=7&a197110p=4&a197110c=10&urltype=tree.TreeTempUrl&wbtreeid=1317',
        'http://jsj.nwpu.edu.cn/new/news.jsp?a197110t=7&a197110p=3&a197110c=10&urltype=tree.TreeTempUrl&wbtreeid=1317',
        'http://jsj.nwpu.edu.cn/new/news.jsp?a197110t=7&a197110p=2&a197110c=10&urltype=tree.TreeTempUrl&wbtreeid=1317',
        # 'http://jsj.nwpu.edu.cn/new/news.jsp?a197110t=7&a197110p=1&a197110c=10&urltype=tree.TreeTempUrl&wbtreeid=1317'
    ]

    base_article_html = "http://jsj.nwpu.edu.cn/info/"  # 文章的基网址
    base_image_html = 'http://jsj.nwpu.edu.cn' # 图片的基网址  # /__local/8/52/49/D2B64688AF6A93E6C054B03A47A_C1969EE8_3F928.jpg


    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        list = response.xpath('/html/body/div[4]/div/div/div[2]/div[2]/div/div/div[2]/div')

        myfilter = Myfilter.MyFilter()
        lasttime = myfilter.FilterbyTime('计算机学院')

        if lasttime:
            timeslist = []
            for tr in list :
                item = ShoolnewsItem()

                item['author'] = '计算机学院'

                # 发布时间
                if len(tr.xpath('./div[1]/div/@class').extract()):
                    h1 = tr.xpath('./div[1]/div/h1/text()').extract()[0].encode('utf-8') # 日期
                    p = tr.xpath('./div[1]/div/p/text()').extract()[0].encode('utf-8') # 年-月
                    date = p + '-' + h1 # 形如 2017-8-7
                    item['posttime'] = datetime.datetime.strptime(date,'%Y-%m-%d')
                    print 'posttimetype: ', type(item['posttime'])
                    print 'posttime : ', item['posttime']

                    # 时间字符串也可以直接比大小
                    if item['posttime'] > lasttime :
                        timeslist.append(item['posttime'])

                        # 文章标题
                        if len(tr.xpath('./div[3]/div/h5/a/text()').extract()) :
                            item['title'] = tr.xpath('./div[3]/div/h5/a/text()').extract()[0].encode('utf-8')
                            print 'title : ', item['title']

                        # 图片网址
                        if len(tr.xpath('./div[2]/div/img/@src').extract()) :
                            item['image_path'] = 'art/' + self.name + hashlib.md5(str(time.clock()).encode('utf-8')).hexdigest() + '.jpg'
                            item['image_html'] = self.base_image_html + tr.xpath('./div[2]/div/img/@src').extract()[0].encode('utf-8')

                            print 'image_path : ', item['image_path']
                            print 'image_html : ', item['image_html']
                        else:
                            item['image_path'] = ''
                            item['image_html'] = ''


                        # 图片地址 文章网址
                        if len(tr.xpath('./div[3]/div/h5/a/text()').extract()) :
                            tempurl = tr.xpath('./div[3]/div/h5/a/@href').extract()[0].encode('utf-8')
                            item['url'] = urljoin(self.base_article_html, tempurl)

                            print 'url : ', item['url']


                            yield scrapy.Request(item['url'], meta=item, dont_filter=True, headers=self.settings.get('DEFAULT_REQUEST_HEADERS'), callback=self.parse_content)

                    else :
                        print '时间爬过了'

            # 循环结束后更新数据表里的时间
            if timeslist:
                latesttime = max(timeslist)
                myfilter.SaveLatestTime(latesttime, '计算机学院')

        else:
            print '数据库中没有lasttime'


    def parse_content(self, response) :
        print "parse_content"
        item = response.meta

        content = ''
        data = response.xpath('//div[@id="vsb_content"]')
        plist = data[0].xpath('string(.)').extract()[0].strip().encode('utf-8')
        for p in plist.splitlines():
            p = p.strip()  # 去掉每行头尾空白
            if not len(p) :
                continue
            p = p + '\n'
            content += p

        item['content'] = content

        return item
