# -*- coding: utf-8 -*-
import scrapy
import sys
from shoolnews.items import ShoolnewsItem

class AutomationSpider(scrapy.Spider):
    name = 'automation'
    allowed_domains = ['zdhxy.nwpu.edu.cn']
    start_urls = ['http://zdhxy.nwpu.edu.cn/xwgg.htm']
    base_url = "http://zdhxy.nwpu.edu.cn/"

    def parse(self, response):
        # 重新设置编码，python2.7的编码问题绝对是超级坑爹的，一天就这样灰飞烟灭了
        # 不过python真的精简。200多行的代码，看了一下别人的规范，不到五十行就能实现了
        reload(sys)
        sys.setdefaultencoding('utf-8')
        #通过response解析出每一条需要查看
        print 'ykl'
        items = []
        list = response.xpath('/html/body/div/div[4]/div[3]/table/tr')
        for tr in list:
            item = ShoolnewsItem()
            if len(tr.xpath('td[2]')):
                item['title'] = tr.xpath('td[2]/a/text()')[0].extract().strip()
                item['time'] = tr.xpath('td[3]/span/text()')[0].extract().strip().encode('utf-8')
                url = tr.xpath('td[2]/a/@href')[0].extract()
                item['url'] = self.base_url+url
                item['content']='1234'
                item['school']='automation'
                items.append(item)
                # print item['title']
                # print item['time']
                # print item['url']
                yield scrapy.Request(item['url'], meta=item, dont_filter=True, headers=self.settings.get('DEFAULT_REQUEST_HEADERS'), callback=self.parse_content)

        # filename = response.url.split('/')[-2] + ".html"
        # with open(filename,'wb') as fp:
        #     fp.write(response.body)

    def parse_content(self, response):
        print "parse_content"
        item = response.meta
        content = ''
        plist = response.xpath('/html/body/div/div[4]/div[3]/form/table/tr[4]/td/div/div/div/table/tbody/tr/td/p')
        for p in plist.xpath('.//text()'):
            content += p.extract().strip()
        item['content'] = content
        return item