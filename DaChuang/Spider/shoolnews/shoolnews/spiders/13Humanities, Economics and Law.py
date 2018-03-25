# -*- coding: utf-8 -*-

'''
人文与经法 Humanities, Economics and Law
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

class HumanitiesSpider(scrapy.Spider):
    name = 'Humanities'
    allowed_domains = ['rwjj.nwpu.edu.cn']

    start_urls = [
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/2.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/3.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/4.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/5.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/6.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/7.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/8.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/9.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/10.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/11.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/12.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/13.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/14.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/15.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/16.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/17.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/18.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/19.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/20.htm',

        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/21.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/22.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/23.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/24.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/25.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/26.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/27.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/28.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/29.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/30.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/31.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/32.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/33.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/34.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/35.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/36.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/37.htm',

        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/38.htm',
        # 'http://rwjj.nwpu.edu.cn/xwgg/xwdt/39.htm',
        'http://rwjj.nwpu.edu.cn/xwgg/xwdt.htm'
    ]

    base_image_html = 'http://rwjj.nwpu.edu.cn'

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        print 'parse....'

        myfilter = Myfilter.MyFilter()
        lasttime = myfilter.FilterbyTime('人文与经法学院')

        print 'lasttime: ', lasttime
        if lasttime:
            timeslist = []

            for i in range(0, 20):  # 左闭右开区间
            # for i in range(1, 21):  # 左闭右开区间
                data = response.xpath('//tr[@id="''line48239_' + str(i) + '"]')

                for tr in data:
                    item = ShoolnewsItem()

                    item['author'] = '人文与经法学院'

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

                                value2 = re.search(r'http://news.nwpu.', temp_url)

                                if value2:
                                    pass
                                else :
                                    value = re.search(r'../../info/', temp_url)
                                    # print value
                                    if value:
                                        item['url'] = urljoin("http://rwjj.nwpu.edu.cn/info/1002/51024.htm", temp_url)
                                    else:
                                        item['url'] = urljoin("http://rwjj.nwpu.edu.cn/info/", temp_url)
                                    print 'title : ', item['title']
                                    print 'url : ', item['url']

                                    yield scrapy.Request(item['url'], meta=item, dont_filter=True,
                                     headers=self.settings.get('DEFAULT_REQUEST_HEADERS'), callback=self.parse_content)
                        else:
                            print '时间爬过了'

            # 循环结束后更新数据表里的时间
            if timeslist:
                latesttime = max(timeslist)
                myfilter.SaveLatestTime(latesttime, '人文与经法学院')

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
