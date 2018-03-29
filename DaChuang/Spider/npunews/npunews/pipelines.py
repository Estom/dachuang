# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import MySQLdb


class NpunewsPipeline(object):
    def process_item(self, item, spider):
        print "mysql_ing"
        DBKWARGS = spider.settings.get('DBKWARGS')
        con = MySQLdb.connect(**DBKWARGS)
        cur = con.cursor()
        # source_id 直接由数字2插入表中

        sql = ("insert into article(title, author, content, image_path, posttime, url, source_id)values(%s,%s,%s,%s,%s,%s,%s)")
        # sql = ("insert into shool_news(title, author, content, image_path, posttime, url, source_id)values(%s,%s,%s,%s,%s,%s,%s)")
        lis = (item['title'], item['author'], item['content'], item['image_path'], item['posttime'], item['url'], 2)
        try:
            cur.execute(sql, lis)
        except Exception, e:
            print "insert error:", e
            con.rollback()
        else:
            con.commit()
        cur.close()
        con.close()
        return item


'''
将图片下载到本地
'''
class ImageNpunewsPipeline(object) :
    def process_item(self, item, spider):
        print '开始下载图片...', item['image_html']

        if len(item['image_html']) :

            try:
                temp_path = 'F:/Innovation Project/WorkNew/dachuang/DaChuang/WebServer/dachuang/upload/'
                path = temp_path + item['image_path']
                image = requests.get(item['image_html'])
                f = open(path, 'wb')
                f.write(image.content)
            except IOError:
                print "Error: 图片下载失败，清空"
                item['image_path'] = ''
                item['image_html'] = ''
                path = ''
            else:
                print "图片下载成功"
                f.close()


        else :
            item['image_path'] = ''
            item['image_html'] = ''
            path = ''


        print 'image_path ', item['image_path']
        print 'path ', path
        print 'image_html ', item['image_html']
        print '结束下载图片...', item['url']


        return item

