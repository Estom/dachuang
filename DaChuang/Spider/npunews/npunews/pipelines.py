# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
# import datetime
#
#
# date = datetime.datetime.now().strftime("%Y-%m-%d %H：%M：%S")#会报错
import time
import MySQLdb
# date = time.strftime("%Y-%m-%d%H:%M:%S")

date = time.strftime("%Y_%m%d %H%M")#允许空格和下划线。 冒号和短杠不行

class NpunewsPipeline(object):#需要在setting.py里设置'coolscrapy.piplines.CoolscrapyPipeline':300
    def process_item(self, item, spider):

        # 获取当前工作目录
        # base_dir = os.getcwd()
        base_dir = 'F:\\Innovation Project\\txt\\'
        projectname = 'news_'

        fiename = base_dir + projectname + date + '.txt'
        # 从内存以追加的方式打开文件，并写入对应的数据
        # 将一个字符串写入文件，如果写入结束，必须在字符串后面加上"\n"，然后f.close()关闭文件
        with open(fiename, 'a') as f:
            f.write(item['title'] + '\n')
            f.write(item['posttime'] + '\n')
            f.write(item['author'] + '\n')
            f.write(item['source'] + '\n')
            f.write(item['url'] + '\n')
            f.write(item['content'] + '\n')
        return item

class MySQLNpunewsPipeline(object):
    def process_item(self, item, spider):
        # print 5
        DBKWARGS = spider.settings.get('DBKWARGS')
        con = MySQLdb.connect(**DBKWARGS)
        cur = con.cursor()
        sql = ("insert into nwpu_news(title,posttime,url,content,author,source)values(%s,%s,%s,%s,%s,%s)")
        lis = (item['title'], item['posttime'], item['url'], item['content'], item['author'], item['source'])
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


class MySQL2NpunewsPipeline():
    # 定义一个类方法from_settings，得到settings中的Mysql数据库配置信息，得到数据库连接池dbpool
    def from_settings(cls, settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # __init__中会得到连接池dbpool
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # process_item方法是pipeline默认调用的，进行数据库操作
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
        query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        return item

    # 插入数据库方法_conditional_insert
    def _conditional_insert(self, tx, item):
        # print item['name']
        sql = "insert into testpictures(name,url) values(%s,%s)"
        params = (item["name"], item["url"])
        tx.execute(sql, params)

    # 错误处理方法_handle_error
    def _handle_error(self, failue, item, spider):
        print failue