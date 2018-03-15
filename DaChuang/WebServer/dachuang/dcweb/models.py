# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
# Create your models here.
# 我觉得这一部分可以将对数据库表和对数据库表的操作封装到一个类当中。

#tag 标签是从文章中通过智能分析获得的参数，标签是不定的。而不是一开始由用户给定的参数
class Tag(models.Model):
    name = models.CharField(max_length=30,verbose_name=u'标签名称')
    number = models.IntegerField(default=0,verbose_name=u'访问量')
    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


#class 表示文章不同的分类，是将文章归类到固定的栏目下边，类别试给定的。
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'分类名称')
    number = models.IntegerField(default=0,verbose_name=u'访问量')
    class Meta:
        verbose_name = u'分类'
        verbose_name_plural = verbose_name
        ordering = ['number', 'id']

    def __unicode__(self):
        return self.name



# source主要是publisher的类别，不固定。西工大微信，西工大官网，***学院新闻网
class Source(models.Model):
    name = models.CharField(max_length=300,verbose_name=u'来源类别')
    class Meta:
        verbose_name = u'发布者类别'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


# publisher信息的发布者，主要是微信公众号主体，各学院账号名称等。
class Publisher(models.Model):
    name = models.CharField(max_length=300,verbose_name=u'发布者名称')
    wechat_id = models.CharField(max_length=300,verbose_name=u'微信号',default='nothing' )
    img = models.ImageField(upload_to='pub',verbose_name=u'图片路径',blank=True,null=True,default='1.jpg')
    source = models.ForeignKey(Source,verbose_name=u'分类')
    intro = models.TextField(verbose_name=u'简介')
    class Meta:
        verbose_name = u'发布者'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name=u'文章标题')
    desc = models.CharField(max_length=300, verbose_name=u'文章描述', blank=True)
    content = models.TextField(verbose_name=u'文章内容')
    img = models.ImageField(upload_to='art',verbose_name=u'图片路径', blank=True, null=True)

    love_count = models.IntegerField(default=0, verbose_name=u'喜欢数')
    click_count = models.IntegerField(default=0, verbose_name=u'点击次数')

    date_publish = models.DateTimeField(auto_now_add=True, verbose_name=u'发布时间')
    tag_mark = models.BooleanField(verbose_name=u'标签标记',default=False,)

    publisher = models.ForeignKey(Publisher, verbose_name=u'发布者')
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name=u'分类')
    tag = models.ManyToManyField(Tag, verbose_name=u'标签',blank=True)
    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def increase_views(self):
        self.click_count +=1
        self.save(update_fields=['click_count'])

    def increase_loves(self):
        self.love_count += 1
        self.save(update_fields=['love_count'])

    def __unicode__(self):
        return self.title



# 每一个UserNormal中包含一个User对象，每一个User对象可以通过get_profile()方法，
# 返回与该对象相关的额外信息
class UserNormal(models.Model):
    STATUS_SIZE = (
        (0, u'男'),
        (1, u'女'),
    )
    user = models.OneToOneField(User)

    sex = models.IntegerField(default=0,blank=True,verbose_name='性别',choices=STATUS_SIZE)
    age = models.IntegerField(default=18,blank=True,verbose_name=u'年龄')

    phone = models.CharField(blank=True, max_length=20, verbose_name=u'电话',default='11011011011')

    desc = models.CharField(max_length=300,verbose_name=u'简介',default=u'小白')
    img = models.ImageField(upload_to='user', verbose_name=u'头像',null=True,default='1.jpg')
    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserNormal.objects.create(user=instance,img='1.jpg',desc=u'小白',phone='11011011011')

post_save.connect(create_user_profile, sender=User)

class History(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    time = models.DateTimeField(verbose_name='时间',auto_now=True)
    class Meta:
        verbose_name = u'历史记录'
        verbose_name_plural = u"浏览历史"

    def add(self,user,article):
        # print not History.objects.filter(user=user,article=article).exists()
        if not History.objects.filter(user=user,article=article).exists():
            print 'what fuck'
            Article.objects.filter(pk=article.pk).update(click_count=article.click_count + 1)

        History.objects.filter(user=user,article=article).delete()
        result = History(user=user,article=article)
        result.save()
        # article_item = Article.objects.get(pk=article)

        # history_list = History.objects.filter(user=user).order_by('time')
        # if len(history_list) > 10:
        #     history_list[0].delete()

    def __unicode__(self):
        return unicode(self.id)

class Love(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    time = models.DateTimeField(verbose_name='时间',auto_now=True)
    class Meta:
        verbose_name = u'喜欢记录'
        verbose_name_plural = u"喜欢"

    def add(self,user,article):
        if not Love.objects.filter(user=user,article=article).exists():
            Article.objects.filter(pk=article.pk).update(love_count=article.love_count + 1)
        Love.objects.filter(user=user,article=article).delete()
        result = Love(user=user,article=article)
        result.save()
        # article_item = Article.objects.get(pk=article)


    def __unicode__(self):
        return unicode(self.id)


class Recommend(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)

    class Meta:
        verbose_name = u'推荐'
        verbose_name_plural = u"推荐"

    def __unicode__(self):
        return unicode(self.id)


class Star(models.Model):
    user = models.ForeignKey(User)
    publisher = models.ForeignKey(Publisher)

    class Meta:
        verbose_name = u'关注'
        verbose_name_plural = u"关注"

    def __unicode__(self):
        return unicode(self.id)


