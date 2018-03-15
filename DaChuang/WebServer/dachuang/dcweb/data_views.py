# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse,render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.template import RequestContext
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import logout, login,authenticate
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from models import Article, Category, Tag, Publisher,UserNormal,Recommend,Star,History,Love,Source
from forms import *
logger = logging.getLogger('blog.views')
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Count
from django.views.decorators.cache import cache_page

# 通过基础的操作知道了一下内容
# list()函数能够将queryset直接转化为普通列表
# values()能见对象转化为字典
# value_list()能将对象转化为元祖
# oder_by()只能通过管理器调用，无法在查询集上调用
@cache_page(60 * 60 * 24) # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
def app_data(request):
    # 传递导视图的数据
    data_dict={}
    #实现了文章热度排行----------------------
    # 获取查询集，并将对象字典化
    hot_article_set = Article.objects.all().values('id','title','publisher','click_count','love_count')
    # 为每一个字典添加热度键值对
    for hot_article in hot_article_set:
        hot_article['hot_num']=hot_article['click_count']+2*hot_article['love_count']
        # try:
        #     print hot_article['hot_num']
        # except IOError:
        #     print u'IO异常'
    # 将查询集转化为列表，并通过匿名函数进行排序。进行切片操作，得到排名前十的文章
    hot_article_list = list(hot_article_set)
    hot_article_list.sort(key=lambda art:art['hot_num'])
    hot_article_list.reverse()
    hot_article_list = hot_article_list[:10]
    # 测试，用来显示内容
    # for p in hot_article_list:
    #     try:
    #         print p['hot_num']
    #     except IOError:
    #         print u'IO异常'

    # 添加到字典当中
    data_dict['hot_article_list']=hot_article_list

    # 发布者被关注排行榜--------------------
    star_publisher_set = Publisher.objects.annotate(num_star=Count('star')).order_by('-num_star')[:10]
    # 测试，用来显示内容
    # for star_publisher in star_publisher_set:
    #     print star_publisher.num_star

    # 添加到字典当中
    data_dict['star_publisher_set'] = star_publisher_set

    # 发布者热度排行--------------------------
    hot_publisher_set = Publisher.objects.all().values('id','name')
    for publisher in hot_publisher_set:
        sum = 0
        article_list = Article.objects.filter(publisher=publisher['id'])
        for article in article_list:
            sum += article.click_count
            sum += 2*article.love_count
        publisher['hot_num']=sum

    hot_publisher_list=list(hot_publisher_set)
    hot_publisher_list.sort(key=lambda pub:pub['hot_num'])
    hot_publisher_list.reverse()
    hot_publisher_list=hot_publisher_list[:10]
    #测试，用来显示内容
    # for publisher in hot_publisher_list:
    #     print 11111
    #     print publisher['hot_num']

    # 添加到字典当中
    data_dict['hot_publisher_list'] = hot_publisher_list

    # 被使用的标签数据排行榜------------------------
    use_tag = Tag.objects.all().order_by('-number')[:10]

    # 添加到字典当中
    data_dict['use_tag'] = use_tag

    # 标签的热度排行榜---------------------------暂缓执行

    # 类别的文章数量分布--------------------------
    category_list = Category.objects.annotate(num_article=Count('article')).order_by('-num_article')

    # 添加到字典当中
    data_dict['category_list'] = category_list

    # 类别的文章热度分布---------------------------
    hot_category_set = Category.objects.all().values('id', 'name')
    for category in hot_category_set:
        sum = 0
        article_list = Article.objects.filter(category=category['id'])
        for article in article_list:
            sum += article.click_count
            sum += 2 * article.love_count
        category['hot_num'] = sum

    hot_category_list = list(hot_publisher_set)
    hot_category_list.sort(key=lambda cat: cat['hot_num'])
    hot_category_list.reverse()
    hot_category_list = hot_category_list[:10]
    #测试，用来显示内容
    # for category in hot_category_list:
    #     print 11111
    #     print category['hot_num']
    # 添加到字典当中
    data_dict['hot_category_list'] = hot_category_list

    # 来源的文章数量分布---------------------------------------
    source_set = Source.objects.all().values()
    for source in source_set:
        sum = 0
        author_list = Publisher.objects.filter(source=source['id'])
        for author in author_list:
            dict = Publisher.objects.filter(id=author.id).aggregate(number=Count('article'))
            sum += dict['number']
        source['article_num']=sum
    # 测试,用来显示内容
    # for source in source_set:
    #     print source['article_num']

    # 添加到字典当中
    data_dict['source_set'] = source_set
    # 来源的文章热度分布--------------------------------
    source_set2 = Source.objects.all().values()
    for source in source_set2:
        sum = 0
        author_list = Publisher.objects.filter(source=source['id'])
        for author in author_list:
            for pub in hot_publisher_list:
                if author.id == pub['id']:
                    sum += pub['hot_num']
                    break
        source['hot_num']=sum
    # 测试,用来显示内容
    # for source in source_set2:
    #     print source['hot_num']

    # 添加到字典当中
    data_dict['source_set2'] = source_set2
    return render(request, 'android/data.xml', data_dict)

# 首先实现参数封装传递过程，这节课必须完成这个东西
# 然后根据页面需要，对参数进行格式化，然后显示出来。
@cache_page(60 * 60 * 24) # 秒数，这里指缓存 一天，不直接写900是为了提高可读性
def data(request):
    # 传递导视图的数据
    data_dict2 = {}
    # 实现了文章热度排行----------------------
    # 获取查询集，并将对象字典化
    hot_article_set = Article.objects.all().values('id', 'title', 'publisher', 'click_count', 'love_count')
    # 为每一个字典添加热度键值对
    for hot_article in hot_article_set:
        hot_article['hot_num'] = hot_article['click_count'] + 2 * hot_article['love_count']
        # try:
        #     print hot_article['hot_num']
        # except IOError:
        #     print u'IO异常'
    # 将查询集转化为列表，并通过匿名函数进行排序。进行切片操作，得到排名前十的文章
    hot_article_list = list(hot_article_set)
    hot_article_list.sort(key=lambda art: art['hot_num'])
    hot_article_list.reverse()
    hot_article_list = hot_article_list[:10]
    # 测试，用来显示内容
    # for p in hot_article_list:
    #     try:
    #         print p['hot_num']
    #     except IOError:
    #         print u'IO异常'

    # 添加到字典当中
    data_dict2['hot_article_list'] = hot_article_list

    # 被使用的标签数据排行榜------------------------
    use_tag = Tag.objects.all().order_by('-number')[:10]

    # 添加到字典当中
    data_dict2['use_tag'] = use_tag

    # 标签的热度排行榜---------------------------暂缓执行

    # 发布者被关注排行榜--------------------
    star_publisher_set = Publisher.objects.annotate(num_star=Count('star')).order_by('-num_star')[:10]
    # 测试，用来显示内容
    # for star_publisher in star_publisher_set:
    #     print star_publisher.num_star

    # 添加到字典当中
    data_dict2['star_publisher_set'] = star_publisher_set

    # 发布者热度排行--------------------------
    hot_publisher_set = Publisher.objects.all().values('id','name')
    for publisher in hot_publisher_set:
        sum = 0
        article_list = Article.objects.filter(publisher=publisher['id'])
        for article in article_list:
            sum += article.click_count
            sum += 2*article.love_count
        publisher['hot_num']=sum

    hot_publisher_list=list(hot_publisher_set)
    hot_publisher_list.sort(key=lambda pub:pub['hot_num'])
    hot_publisher_list.reverse()
    hot_publisher_list=hot_publisher_list[:10]
    #测试，用来显示内容
    # for publisher in hot_publisher_list:
    #     print 11111
    #     print publisher['hot_num']

    # 添加到字典当中
    data_dict2['hot_publisher_list'] = hot_publisher_list

    # 类别的文章数量分布--------------------------
    category_list = Category.objects.annotate(num_article=Count('article')).order_by('-num_article')

    # 添加到字典当中
    data_dict2['category_list'] = category_list

    # 类别的文章热度分布---------------------------
    hot_category_set = Category.objects.all().values('id', 'name')
    for category in hot_category_set:
        sum = 0
        # print category['name']
        article_list = Article.objects.filter(category=category['id'])
        for article in article_list:
            sum += article.click_count
            sum += 2 * article.love_count
        category['hot_num'] = sum

    hot_category_list = list(hot_category_set)
    hot_category_list.sort(key=lambda cat: cat['hot_num'])
    hot_category_list.reverse()
    hot_category_list = hot_category_list[:10]
    # 测试，用来显示内容
    # for category in hot_category_list:
    #     print 11111
    #     print category['hot_num']
    # 添加到字典当中
    data_dict2['hot_category_list'] = hot_category_list

    # 来源的文章数量分布---------------------------------------
    source_set = Source.objects.all().values()
    for source in source_set:
        sum = 0
        author_list = Publisher.objects.filter(source=source['id'])
        for author in author_list:
            dict = Publisher.objects.filter(id=author.id).aggregate(number=Count('article'))
            sum += dict['number']
        source['article_num'] = sum
    # 测试,用来显示内容
    # for source in source_set:
    #     print source['article_num']

    # 添加到字典当中
    data_dict2['source_set'] = source_set
    # 来源的文章热度分布--------------------------------
    source_set2 = Source.objects.all().values()
    for source in source_set2:
        sum = 0
        author_list = Publisher.objects.filter(source=source['id'])
        for author in author_list:
            for pub in hot_publisher_list:
                if author.id == pub['id']:
                    sum += pub['hot_num']
                    break
        source['hot_num'] = sum
    # 测试,用来显示内容
    # for source in source_set2:
    #     print source['hot_num']

    # 添加到字典当中
    data_dict2['source_set2'] = source_set2
    return render(request, 'blog/data.html',data_dict2)