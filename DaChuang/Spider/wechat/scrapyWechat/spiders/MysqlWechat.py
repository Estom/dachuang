# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class mysqlwechat(object):
    def getUser(self):
        print "get list of user"
        con = MySQLdb.connect(host='111.230.181.121',
                                port=3306,
                                user='root',
                                passwd='ykl123',
                                db='dcserver',
                                charset='utf8'
                              )
        cur = con.cursor()
        print 'hello'
        wechatList = []
        sql = "SELECT name,wechat_id FROM dcweb_publisher where source_id=1"
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                res = (row[0],row[1])
                wechatList.append(res)
        except Exception, e:
            print "insert error:", e
            con.rollback()
        else:
            con.commit()
        cur.close()
        con.close()
        return wechatList

mw = mysqlwechat()
print mw.getUser()

