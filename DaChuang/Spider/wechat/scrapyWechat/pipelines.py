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
        sql = ("insert into article(title,author,`desc`,content,posttime,image_path,url,source_id)values(%s,%s,%s,%s,%s,%s,%s,%s)")
        lis = (item['title'], item['author'], item['desc'], item['content'], item['posttime'], item['image_path'], item['url'], item['source_id'])
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
