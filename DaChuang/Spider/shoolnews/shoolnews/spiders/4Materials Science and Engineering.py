# -*- coding: utf-8 -*-

'''
材料  Materials Science and Engineering
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

"""
材料学院的新闻大部分在新闻网的校园动态上发布，个人认为单独爬材料学院没有必要!!!
"""

class MaterialsScienceSpider(scrapy.Spider):
    name = 'MaterialsScience'
    allowed_domains = ['cailiao.nwpu.edu.cn']

    start_urls = [
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/2.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/3.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/4.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/5.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/6.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/7.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/8.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/9.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/10.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/11.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/12.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/13.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/14.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/15.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/16.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/17.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/18.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/19.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/20.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/21.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/22.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/23.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/24.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/25.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/26.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/27.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/28.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/29.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/30.htm',


        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/31.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/32.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/33.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/34.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/35.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/36.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/37.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/38.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/39.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/40.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/41.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/42.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/43.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/44.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/45.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/46.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/47.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/48.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/49.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/40.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/41.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/42.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/43.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/44.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/45.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/46.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/47.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/48.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/49.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/50.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/51.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/52.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/53.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/54.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/55.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/56.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/57.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/58.htm',

        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/60.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/61.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/62.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/63.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/64.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/65.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/66.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/67.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/68.htm',
        # 'http://cailiao.nwpu.edu.cn/zw2017/zxxx/69.htm',
        'http://cailiao.nwpu.edu.cn/zw2017/zxxx.htm',
    ]

    base_image_html = 'http://cailiao.nwpu.edu.cn'

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        print 'parse....'

        myfilter = Myfilter.MyFilter()
        lasttime = myfilter.FilterbyTime('材料学院')

        print 'lasttime: ', lasttime
        if lasttime:
            timeslist = []
            for i in range(0, 10):  # 左闭右开区间
            # for i in range(6, 16):  # 左闭右开区间
                data = response.xpath('//tr[@id="''line193659_' + str(i) + '"]')

                for tr in data:
                    item = ShoolnewsItem()

                    item['author'] = '材料学院'

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
                                print value2
                                if value2:
                                    pass
                                else :
                                    value = re.search(r'../../info/', temp_url)
                                    # print value
                                    if value:
                                        item['url'] = urljoin("http://cailiao.nwpu.edu.cn/info/1002/51024.htm", temp_url)
                                    else:
                                        item['url'] = urljoin("http://cailiao.nwpu.edu.cn/info/", temp_url)
                                    print 'title : ', item['title']
                                    print 'url : ', item['url']

                                    yield scrapy.Request(item['url'], meta=item, dont_filter=True,
                                     headers=self.settings.get('DEFAULT_REQUEST_HEADERS'), callback=self.parse_content)
                        else:
                            print '时间爬过了'

            # 循环结束后更新数据表里的时间
            if timeslist:
                latesttime = max(timeslist)
                myfilter.SaveLatestTime(latesttime, '材料学院')

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
