# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import requests
import os
from PIL import Image
from io import BytesIO


class ScrapywechatPipeline(object):
    def process_item(self, item, spider):
        print "mysql_ing"
        DBKWARGS = spider.settings.get('DBKWARGS')
        con = MySQLdb.connect(**DBKWARGS)
        cur = con.cursor()
        sql = ("insert into article(title,author,`desc`,content,image_path,posttime,url,source_id)values(%s,%s,%s,%s,%s,%s,%s,%s)")
        # sql = ("insert into shool_news(title, author, `desc`, content, image_path, posttime, url, source_id)values(%s,%s,%s,%s,%s,%s,%s,%s)")
        lis = (item['title'], item['author'], item['desc'], item['content'], item['image_path'], item['posttime'], item['url'], item['source_id'])

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
class ImageScrapywechatPipeline(object) :
    def process_item(self, item, spider):
        print '开始下载图片...', item['image_html']

        if len(item['image_html']) :
            try:
                # temp_path = 'F:/Innovation Project/WorkNew/dachuang/DaChuang/WebServer/dachuang/upload/'

                # 改为相对路径
                temp_path = os.path.abspath('../..') + '/WebServer/dachuang/upload/'

                path = temp_path + item['image_path']
                response = requests.get(item['image_html'])
                image = Image.open(BytesIO(response.content))
                # print image.size[0]
                width = int(image.size[0])
                height = int(image.size[1])
                out = image.resize((width, height),Image.ANTIALIAS)  # resize image with high-quality
                out.save(path)

                # f = open(path, 'wb')
                # f.write(image.content)

                if (os.path.exists('/var/www/html/dachuang/upload/art')):
                    print '图片保存到服务器'
                    temp_path_linux = '/var/www/html/dachuang/upload/' + item['image_path']  # 'image_path'：atr/xxxx.jpg
                    out.save(temp_path_linux)
            except IOError:
                print "Error: 图片下载失败，清空"
                item['image_path'] = ''
                item['image_html'] = ''
                path = ''

            else:
                print "图片下载成功"
                # f.close()


        else :
            item['image_path'] = ''
            item['image_html'] = ''
            path = ''

        print 'image_path ', item['image_path']
        print 'path ', path
        print 'image_html ', item['image_html']
        print '结束下载图片...', item['url']

        return item