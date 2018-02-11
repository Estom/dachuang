# -*- coding: utf-8 -*-

import MySQLdb

class MyFilter(object):
    def __init__(self):
        self._conn = MySQLdb.connect(host='111.230.181.121',
                              port=3306,
                              user='root',
                              passwd='ykl123',
                              db='dcserver',
                              charset='utf8'
                              )
        self._cursor = self._conn.cursor()

    def FilterbyTime(self, name):
        print "FilterbyTime...."


        '''数据表的编码是utf-8'''
        name = name.encode("utf-8")
        print 'name: ', name

        result = ''
        sql = 'select lasttime from dcweb_publisher where name = "%s"' % name

        try:
            self._cursor.execute(sql)
            temp = self._cursor.fetchone()
            # result是tuple类型，result ：(datetime.datetime(2018, 1, 31, 0, 0),)
            print 'temptype: ', type(temp)
            print 'temp: ', temp

            # result = temp[0].strftime('%Y-%m-%d')

            result = temp[0]
            print 'type(temp[0]): ', type(temp[0])
            # print 'type(result): ', type(result)
            print 'result: ', result

        except Exception, e:
            print "select error:", e
            self._conn.commit()
        else:
            self._conn.commit()

        return result


    def SaveLatestTime(self, latesttime, name):
        print "SaveLatestTime...."

        sql = 'update dcweb_publisher set lasttime ="%s" where name = "%s"' % (latesttime, name)

        try:
            print 'latesttime: ', latesttime
            self._cursor.execute(sql)
        except Exception, e:
            print "select error:", e
            self._conn.commit()
        else:
            self._conn.commit()
