# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class ScrapywechatPipeline(object):
    def process_item(self, item, spider):
        print "mysql_ing"
        DBKWARGS = spider.settings.get('DBKWARGS')
        con = MySQLdb.connect(**DBKWARGS)
        cur = con.cursor()
        sql = ("insert into wechat_article(title,author,abstract,content_url,cover,datetime,content_real,body_html)values(%s,%s,%s,%s,%s,%s,%s,%s)")
        lis = (item['title'], item['author'], item['abstract'], item['content_url'], item['cover'], item['datetime'], item['content_real'], item['body_html'])
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
