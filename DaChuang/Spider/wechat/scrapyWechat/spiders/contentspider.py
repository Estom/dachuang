# -*- coding: utf-8 -*-
import scrapy
import wechatsogou
from scrapyWechat.items import ScrapywechatItem
from MysqlWechat import mysqlwechat
import sys
import os
import time
from datetime import datetime
import Myfilter
import time
import hashlib
"""
            '瓜大人文微助手':'guada-renwen',
            '空院微视野':'nwpuhangkong',
            '小齿轮':'nwpujdsu',
            '软芯微语':'ruanxinweiyu',
            '小瓜工大助手':'npuxiaogua',
            '工大瓜籽汇':'npuguazi',
            '西北工业大学':'npustar',
            '西工大就业':'nwpujob',
            '西北工业大学图书馆':'nwpu-lib',
            '西工大英语竞赛':'npuenglishevents',
            '西工大航模队':'nwpu-amt',
            '西工大招办':'zsbnwpu',
            '西北工业大学学生注册中心':'nwpuxszczx',
            '西工大大学生新闻中心':'npudaily',
"""

class ContentspiderSpider(scrapy.Spider):
    name = 'contentspider'

    allowed_domains = ['mp.weixin.qq.com',
                       'weixin.sogou.com',
                       'baidu.com'
    ]

    start_urls = ['http://weixin.sogou.com/']

    def start_requests(self):
        reqs = []

        user = mysqlwechat()

        NWPUWechatIDList = user.getUser()


        ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=2,)

        for author,wechat_id in NWPUWechatIDList:
            print 'wechat_id:',wechat_id
            print 'author:',author

            try:
                time.sleep(6)

                myfilter = Myfilter.MyFilter()
                lasttime = myfilter.FilterbyTime(author)

                print 'lasttime: ', lasttime
                timeslist = []

                result_from_history = ws_api.get_gzh_article_by_history(wechat_id)
                article_result_list = result_from_history.get("article")

                item = ScrapywechatItem()

                for article_result in article_result_list:
                    item["posttime"] = datetime.fromtimestamp(article_result.get("datetime"))
                    if item["posttime"] > lasttime:
                        timeslist.append(item['posttime'])

                        item["title"] = article_result.get("title")
                        item["url"] = article_result.get("content_url")
                        item["desc"] = article_result.get("abstract")
                        item["author"] = author
                        item["image_html"] = article_result.get("cover")
                        item['image_path'] = 'art/' + self.name + hashlib.md5(
                            str(time.clock()).encode('utf-8')).hexdigest() + '.jpg'
                        item["source_id"] = 1

                        print 'title : ', item["title"]
                        print 'author : ', item["author"]
                        print 'posttime : ', item["posttime"]
                        print 'url : ', item["url"]
                        print 'image_html : ', item["image_html"]
                        print 'image_path : ', item["image_path"]
                        req = scrapy.Request(article_result.get("content_url"), meta=item, dont_filter=True, headers=self.settings.get('DEFAULT_REQUEST_HEADERS'))
                        reqs.append(req)
                        print '-------'
                    else:
                        print '时间爬过了'
                        continue

                # 循环结束后更新数据表里的时间
                if timeslist:
                    latesttime = max(timeslist)
                    myfilter.SaveLatestTime(latesttime, author)

            except Exception,e:
                print 'error occur when get the url of wechat publisher'
                print e
            else:
                print 'successful get the url of the publisher'

        return reqs



    def parse(self, response):
        print sys.getdefaultencoding()

        # 重新设置编码，python2.7的编码问题绝对是超级坑爹的，一天就这样灰飞烟灭了
        # 不过python真的精简。200多行的代码，看了一下别人的规范，不到五十行就能实现了
        reload(sys)
        sys.setdefaultencoding('utf-8')

        item = response.meta


        # print u"标题:", response.xpath('//*[@id="activity-name"]/text()')[0].extract().strip()
        # print u"时间:", response.xpath('string(//*[@id="post-date"])')[0].extract().strip()
        # if len(response.xpath('//*[@id="meta_content"]/em[2]/text()')) != 0:
        #     print u"小组:", response.xpath('//*[@id="meta_content"]/em[2]/text()')[0].extract().strip()
        # print u"公众号:", response.xpath('//*[@id="meta_content"]/span/text()')[0].extract().strip()
        #
        # if len(response.xpath('string(//*[@id="js_content"])')) == 0:
        #     print u"测试", response.xpath('string(//*[@id="img-content"]/div[2])')[0].extract().strip()
        # else:
        #     tt = response.xpath('string(//*[@id="js_content"])').extract()[0]
        #     print u'内容',tt
# 经过坚持不懈的验证，得出一个结论，这里应该是pythonUnicode编码存在的错误
# 也就是说，返回的数据都是正确，而且也会有Unicode编码的正常数据，但在extract之后
# 如果输出的事中文，数组中的Unicode字符会报错，导致异常退出，也就是说，print解码或者保存会出错。
# 通过shell命令也能输出Unicode原码，说明数据本身没有问题，也能将Unicode原码打印到控制台，但是不能保存到文件
# 在shell下的不能保存到控制台应该和这里的不能打印或者不能保存有同样的理由。都是因为不同文章的编码方式不同
# 导致一些文章在编码的时候出错，不过保存到数据库真的有影响吗，可以尝试一下。
# 白死不得其解的是，为什么有几个网页不能看，而其他的都没有问题，真的不爽啊这就说明错误还跟网页的具体内容有关？？？

        title = response.xpath('//*[@id="activity-name"]/text()')[0].extract().strip()
        time = response.xpath('string(//*[@id="post-date"])')[0].extract().strip()
        if len(response.xpath('//*[@id="meta_content"]/em[2]/text()')) != 0:
            group = response.xpath('//*[@id="meta_content"]/em[2]/text()')[0].extract().strip()
        else:
            group = ""
        publication = response.xpath('//*[@id="meta_content"]/span/text()')[0].extract().strip()
        content = response.xpath('string(//div[@id="js_content"])').extract()[0].strip().encode('utf-8')

        content_real = title + "\n" + time + "\n" + group + "\n" + publication + "\n" + content + "\n"

        item["content"] = content_real
        # 此处省略对content_real从body中解析出来的过程
        return item
