# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import requests

class ShoolnewsPipeline(object):
    def process_item(self, item, spider):
        print "mysql_ing"
        DBKWARGS = spider.settings.get('DBKWARGS')
        con = MySQLdb.connect(**DBKWARGS)
        cur = con.cursor()
        sql = ("insert into shool_news(shool,title,time,content,content_html,image_path,image_html)values(%s,%s,%s,%s,%s,%s,%s)")
        lis = (item['school'], item['title'], item['time'], item['content'], item['url'], item['image_path'], item['image_html'])
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
class ImageShoolnewsPipeline(object) :
    def process_item(self, item, spider):
        print 'load image...'
        imagehtml = item['image_html']

        path = item['image_path'].encode('gb2312')

        image = requests.get(imagehtml)
        f = open(path, 'wb')
        f.write(image.content)
        f.close()

        return item
