# 数据库的配置

在settings中找到DBKWARGS配置成自己的数据库，并且创建表格scrapy_wechat_article ，方能使用数据库。



# 关联的python库

scrapy

MySQLdb

wechatsogou



# 启动命令

scrapy crawl contentspider


# 关于验证码问题

当在命令行中执行需要验证码的时候，根据弹出的图片填写，两次重试机会


# 其他配置

关于爬虫延迟、终止、报文头、代理配置请参考官方说明书