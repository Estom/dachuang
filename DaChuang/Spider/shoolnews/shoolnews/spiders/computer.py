# -*- coding: utf-8 -*-

'''
计算机 Computer Science and Technology
'''


import scrapy
import sys
import os
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin

class ComputerSpider(scrapy.Spider) :
    name = 'computer'
    allowed_domains = ['jsj.nwpu.edu.cn']
    start_urls = ['http://jsj.nwpu.edu.cn/new/news.jsp?a197110t=7&a197110p=2&a197110c=10&urltype=tree.TreeTempUrl&wbtreeid=1317']

    base_article_html = "http://jsj.nwpu.edu.cn/info/"  # 文章的基网址
    base_image_html = 'http://jsj.nwpu.edu.cn' # 图片的基网址  # /__local/8/52/49/D2B64688AF6A93E6C054B03A47A_C1969EE8_3F928.jpg

    base_path = 'C:/Images/' # 图片保存到本地的基地址


    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')

        list = response.xpath('/html/body/div[4]/div/div/div[2]/div[2]/div/div/div[2]/div')

        for tr in list :
            item = ShoolnewsItem()

            item['school'] = '计算机学院'

            # 图片网址
            if len(tr.xpath('./div[2]/div/img/@src').extract()) :
                item['image_html'] = self.base_image_html + tr.xpath('./div[2]/div/img/@src').extract()[0].encode('utf-8')
                print 'image_html : ', item['image_html']

            # 建立文件夹'C:/Images/计算机学院'
            fileName = self.base_path + item['school'].encode('gb2312')
            if not os.path.exists(fileName):
                os.makedirs(fileName)

            # 文章标题 文章网址
            if len(tr.xpath('./div[3]/div/h5/a/text()').extract()) :
                item['title'] = tr.xpath('./div[3]/div/h5/a/text()').extract()[0].encode('utf-8')
                item['image_path'] = 'C:/Images/计算机学院/' + item['title'] + '.jpg'

                tempurl = tr.xpath('./div[3]/div/h5/a/@href').extract()[0].encode('utf-8')
                item['url'] = urljoin(self.base_article_html, tempurl)

                print 'title : ', item['title']
                print 'url : ', item['url']
                print 'image_path : ', item['image_path']

                yield scrapy.Request(item['url'], meta=item, dont_filter=True, headers=self.settings.get('DEFAULT_REQUEST_HEADERS'), callback=self.parse_content)


    def parse_content(self, response) :
        print "parse_content"
        item = response.meta

        data = response.xpath('//div[@id="vsb_content"]')
        item['content'] = data[0].xpath('string(.)').extract()[0].strip().encode('utf-8')


        data1 = response.xpath('//span[@class="c141088_date"]')
        item['time'] = data1[0].xpath('text()').extract()[0].encode('utf-8')

        return item
