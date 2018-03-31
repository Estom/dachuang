# 基于网络爬虫和数据分析的高校信息整合平台
> 这个项目目的在于开发一个简洁，智能，高效的内容阅读平台，构建校园信息生态圈，提供一种更
加优雅合理的信息获取方式。本平台的所有数据均通过合法方式从校园内的各大信息来源获取，分成
四大独立的模块，由不同人主要负责哥哥模块，定制模块之间的接口。

## 项目说明

工程主要包括五个部分，三个已经完成的出部分：**网络爬虫**，**数据分析**，**服务器**。
还有两个部分仍旧在进行。包括：**文档说明**，**Android**。

## 版本说明
Version 1.0
* 实现了 巴拉巴拉

Version 2.0
* 实现了巴拉巴拉

Version 3.0
* 实现了巴拉巴拉


## 任务列表
### 爬虫
> 从西北工业大学官网，西北工业大学学院网和微信三部分获取数据，并进行筛选和格式化。文章
最后保留字段为：title,author,category,author,content,time。


~~:fa-check-square-o:工大新闻网基础信息获取~~

~~:fa-check-square-o:各个学院基础信息获取~~

~~:fa-check-square-o:搜狗微信的爬虫~~

~~:fa-check-square-o:图片获取~~

~~:fa-check-square-o:增量爬虫~~

~~:fa-check-square-o:公众号扩展~~

:fa-square-o:爬虫通过脚本自动化运行

### 数据分析
> 对源数据进行加工，包括生成自动摘要，对文章分类，生成标签云，根据用户浏览记录和文章
内容进行智能推荐。最后将加工后的数据从源数据库搬迁到服务器数据库当中。

~~:fa-check-square-o:自动分类~~

~~:fa-check-square-o:自动摘要~~

~~:fa-check-square-o:热词提取~~

~~:fa-check-square-o:基于内容的智能推荐~~

:fa-square-o:基于用户的智能推荐

:fa-square-o:爬虫部分的验证码问题和异常处理问题。

:fa-square-o:数据分析部分的增量运行

### 服务器
> 使用B/S模式搭建了网络服务。从数据库中获取数据，根据用户的访问网址进行路由，对数据进行
渲染，最终通过浏览器界面，用户可以获得相应的服务。

~~:fa-check-square-o:数据库搭建~~

~~:fa-check-square-o:基础信息呈现~~

~~:fa-check-square-o:网站部署（域名服务器申请和搭建Django服务器）~~

~~:fa-check-square-o:数据统计页面实现~~

~~:fa-check-square-o:ndroid访问接口~~

:fa-square-o:页面优化

:fa-square-o:性能优化，提高访问速度

### Android
> 为了使得客户端访问更加高效，界面更加友好，制作了Android客户端。

~~:fa-check-square-o:基础信息呈现~~

~~:fa-check-square-o:页面逻辑实现~~

~~:fa-check-square-o:数据库信息获取~~

:fa-square-o:界面优化

:fa-square-o: 性能优化

:fa-square-o:产品发布


### 文档说明
> 主要包括开发过程中的需求文档，设计说明文档，用户说明文档，问题解决文档等。

[Wiki文档](https://gitee.com//nwpu_dachuang/dachuang/wikis/pages?title=Home&parent=)


## Bug List
> 任何测试中产生的bug都应该在wiki文档中说明，并说明修改要求，完成bug之后，关闭bug。
> 在这里值写出已完成的bug列表和待解决的bug列表，并提供相关链接
> 未完成的bug使用ISSUE功能，提出问题，并进行详细说明和讨论。提供ISSUE问题的链接
> 已完成的bug，使用WIKI功能，建立bug说明文档，描述bug的提出，详情，修改过程，完成效果等。提供WIKI文档链接

~~:fa-bug:[Bug1](https://gitee.com//nwpu_dachuang/dachuang/wikis/pages?title=BUG1&parent=Bug)~~



## 项目依赖

python >= 2.7.13
pillow = 5.0.0


### Analysis

### Spider
wechatsogou = 

Scrapy = 1.4.0

### WebServer

Django = 1.11.9

bootstrap-admin = 0.3.8

mysql-python = 1.2.5

### Android


