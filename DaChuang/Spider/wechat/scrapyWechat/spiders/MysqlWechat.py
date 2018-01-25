# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb



class mysqlwechat(object):
    host = "localhost"
    dbname = "dcspider"
    username = "root"
    password = "ykl123"
    def getUser(self):
        print "get list of user"
        con = MySQLdb.connect("localhost", "root", "ykl123","dcspider")
        cur = con.cursor()

        wechatList = []

        sql = "SELECT wechat_id FROM wechat_user"
        try:
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                wechatList.append(row[0])
        except Exception, e:
            print "insert error:", e
            con.rollback()
        else:
            con.commit()
        cur.close()
        con.close()
        return wechatList

# mw = mysqlwechat()
# print mw.getUser()

