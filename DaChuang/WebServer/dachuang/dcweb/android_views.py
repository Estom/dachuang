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
from models import Article, Category, Tag, Publisher,UserNormal,Recommend,Star,History
from forms import *
logger = logging.getLogger('blog.views')
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse

class IndexView(ListView): # index首页view

    template_name = "android/index.xml"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter()
        #因为没有使用markdown
        #for article in article_list:
            #article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        #kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('-number')[:10]
        return super(IndexView, self).get_context_data(**kwargs)

class IndexRecView(ListView): # index首页所有文章

    template_name = "android/index.xml"
    context_object_name = "article_list"

    user = UserNormal()

    def get(self, request, *args, **kwargs):
        print 456456
        self.user = request.user
        if not request.user.is_authenticated():
            print 11111
            return redirect(reverse('app_login'))

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        print 456
        print self.user
        rec_list = Recommend.objects.filter(user=self.user)
        article_list = []
        for rec in rec_list:
            article_list.append(rec.article)
        #因为没有使用markdown
        #for article in article_list:
            #article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        print 123
        kwargs['category_list'] = Category.objects.all().order_by('name')
        #kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('-number')[:10]
        return super(IndexRecView, self).get_context_data(**kwargs)

class IndexStarView(ListView): # index首页关注文章view
    template_name = "android/index.xml"
    context_object_name = "article_list"

    user = UserNormal()

    def get(self, request, *args, **kwargs):
        self.user = request.user
        if not request.user.is_authenticated():
             return redirect(reverse('app_login'))

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        print 456
        print self.user
        star_list = Star.objects.filter(user=self.user)
        article_list = []
        pub_list = []
        for star in star_list:
            pub_list.append(star.publisher)

        for pub in pub_list:
            article_in_pub = Article.objects.filter(publisher=pub)
            article_list +=article_in_pub
        #因为没有使用markdown
        #for article in article_list:
            #article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        print 123
        kwargs['category_list'] = Category.objects.all().order_by('name')
        #kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('-number')[:10]
        return super(IndexStarView, self).get_context_data(**kwargs)


# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            print 444
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                    email=reg_form.cleaned_data["email"],
                                    password=make_password(reg_form.cleaned_data["password"]),)
                user.save()
                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect(reverse('app_index'))
            else:
                return render(request, 'android/form_failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        print e
        logger.error(e)
    return render(request, 'android/register.xml', locals())

# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'android/form_failure.xml', {'reason': '登录验证失败'})
                return redirect(reverse('app_index'))
            else:
                return render(request, 'android/form_failure.xml', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'android/login.xml', locals())

# 注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        print e
    return redirect(reverse('app_index'))

# 测试
# def test(request):
#     # 经过验证发现，这个玩意的确可以使用系统的用户session进行验证。
#     user = authenticate(username='estom', password='ykl123ykl123')
#     message={}
#     if user is not None:
#         message['message'] = 'there is user'
#         message['username'] = 'estom'
#     else:
#         message['message'] = 'there is no user login'
#
#     # 现在使用request中携带的User对象完成权限认证
#     if request.user.is_authenticated():
#         message['message'] = 'some user is have logined'
#         message['username'] = request.user.username
#     else:
#         message['message'] = 'no one is use the system'
#
#     # 现在验证登录功能的实现
#
#     # 现在验证登出系统的实现
#     return render(request,'error.html',message)


def PersonView(request):
    if request.user.is_authenticated():
        user_normal = UserNormal()
        pub_list = []
        history_list=[]
        try:
            user_normal = UserNormal.objects.get(user = request.user)
            star_list = Star.objects.filter(user=request.user)
            for star in star_list:
                pub_list.append(star.publisher)
            article_in_history = History.objects.filter(user=request.user)
            for his in article_in_history:
                history_list.append(his.article)

        except Exception as e:
            print 'nothing in the database'
            return render(request,'android/person.xml',{'user_normal': user_normal,'pub_list':pub_list,'history_list':history_list})
        return render(request,'android/person.xml',{'user_normal': user_normal,'pub_list':pub_list,'history_list':history_list})
    else:
        return redirect(reverse('app_login'))

# 更新数据的功能已经能够实现。唔觉得还是使用这个函数比较好。
# 因为这个函数与模型直接对接，比自己配置表单验证要简单很多。
def update_data(request):
    if request.method == 'POST':
        print 'ykl'
        form = PersonsForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user_normal = UserNormal.objects.filter(user=request.user).delete()
            user_normal = form.save(commit=False)
            user_normal.user = request.user
            user_normal.save()
            print user_normal.img.url

            return HttpResponseRedirect(reverse('app_person'),RequestContext(request))
    else:
        form = PersonsForm()
    return render(request,'android/person_edit.xml', {'form': form})

# 点赞
def love(request):
    article_id = request.GET['article_id']
    if not request.session.get('has_loved'+article_id, False):
        article = Article.objects.get(id=article_id)
        article.increase_loves()
        request.session['has_loved'+article_id] = True
        print 123
    return redirect(reverse('app_detail',kwargs={'article_id':article_id}))

# 关注
def staring(reqeust):
    pub_id = reqeust.GET['pub_id']
    pub = Publisher.objects.get(id=pub_id)
    star = Star.objects.get_or_create(user=reqeust.user,publisher=pub)
    return redirect(reverse('app_pub_detail',kwargs={'pub_id':pub_id}))

def staroff(reqeust):
    pub_id = reqeust.GET['pub_id']
    pub = Publisher.objects.get(id=pub_id)
    print 'this is off star'
    Star.objects.filter(user=reqeust.user,publisher=pub).delete()
    return redirect(reverse('app_pub_detail',kwargs={'pub_id':pub_id}))

# 修改
def PersonEdit(request):
    try:
        if request.method == 'POST':
            person_form = PersonForm(request.POST, request.FILES or None)
            if person_form.is_valid():
                cd = person_form.cleaned_data
                img_url = person_form['img']
                # 注册
                print cd
                print 'url:'+img_url
                user_normal = UserNormal.objects.get_or_create(user=request.user)
                user_normal.sex=person_form.cleaned_data["username"]
                user_normal.age=person_form.cleaned_data["email"]
                user_normal.phone=person_form.cleaned_data["phone"]
                user_normal.desc = person_form.cleaned_data["desc"]
                user_normal.img=person_form.cleaned_data["img"]
                user_normal.save()
                return redirect(reverse('app_person'))
            else:
                return render(request, 'android/form_failure.html', {'reason': person_form.errors})
        else:
            person_form = PersonForm()
    except Exception as e:
        print e
        logger.error(e)
    return render(request, 'android/person_edit.xml', locals())



class ArticleDetailView(DetailView): # detail  view 文章详细
    model = Article
    template_name = "android/detail.xml"
    context_object_name = "article"

    # pk_url_kwarg 用于接受一个来自URL的主键，然后会根据这个主键进行查询，我们在之前urlpatterns中已经捕获了article_id
    pk_url_kwarg = 'article_id'

    def get(self, request, *args, **kwargs):
        article = super(ArticleDetailView, self).get_object()
        if request.user.is_authenticated():
            his = History().add(request.user,article)
        return super(ArticleDetailView, self).get(self,request,*args,**kwargs)
    # get_object返回该视图要显示的对象。若果设置了queryset，则查询结果就是数据源。如果没有设置queryset，查询视图中
    # 的pk_url_kwarg，以它为主键进行查询，返回查询结果
    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.increase_views()
        # obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        return obj

    # 第五周新增
    # def get_context_data(self, **kwargs):
    #     kwargs['comment_list'] = self.object.blogcomment_set.all()
    #     kwargs['form'] = BlogCommentForm()
    #     return super(ArticleDetailView, self).get_context_data(**kwargs)





class CategoryView(ListView):  # index view 文章
    template_name = "android/index.xml"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'])
        # for article in article_list:
        #     article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )

        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['tag_list'] = Tag.objects.all().order_by('-number')[:10]
        return super(CategoryView, self).get_context_data(**kwargs)


class TagView(ListView): #index article_list 云标签
    template_name = "android/index.xml"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(tag=self.kwargs['tag_id'])
        # for article in article_list:
        #     article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['tag_list'] = Tag.objects.all().order_by('-number')[:10]
        return super(TagView, self).get_context_data(**kwargs)


class PublishView(ListView): # 发布者列表
    template_name = "android/pub_list.xml"
    context_object_name = "pub_list"

    def get_queryset(self):
        pub_list = Publisher.objects.all()
        # pub_list = pub_list[:2]
        # for pub in pub_list:
        #     pub.img = Image.objects.get(id=pub.img)
        # for article in article_list:
        #     article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return pub_list

    def get_context_data(self, **kwargs):
        return super(PublishView, self).get_context_data(**kwargs)


class PubDetailView(ListView): # index article_list 云标签
    template_name = "android/pub_detail.xml"
    context_object_name = "article_list"
    article_num = 0
    user = User()
    stared=True
    loged =True
    def get(self, request, *args, **kwargs):
        user = request.user
        pubb= Publisher.objects.get(id=self.kwargs['pub_id'])
        star = []
        if not request.user.is_authenticated():
            self.loged =False
            self.stared=False
        else:
            star = Star.objects.filter(user=request.user,publisher=pubb)
        print 123
        print star
        if len(star) == 0:
            print 456
            self.stared = False

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        article_list = Article.objects.filter(publisher=self.kwargs['pub_id'])
        for article in article_list:
            self.article_num += 1
        # for article in article_list:
        #     article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['pub'] = Publisher.objects.get(id=self.kwargs['pub_id'])
        kwargs['article_num'] = self.article_num
        kwargs['stared'] = self.stared
        kwargs['loged'] = self.loged
        return super(PubDetailView, self).get_context_data(**kwargs)


class DataView(ListView):
    template_name = "android/data.xml"
    context_object_name = "article"
    a = 1
    def get_queryset(self):
        pub_list = Publisher.objects.all()
        # pub_list = pub_list[:2]
        # for pub in pub_list:
        #     pub.img = Image.objects.get(id=pub.img)
        # for article in article_list:
        #     article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return pub_list

    def get_context_data(self, **kwargs):
        return super(DataView, self).get_context_data(**kwargs)

#
# class ArchiveView(ListView):
#     template_name = "blog/index.html"
#     context_object_name = "article_list"
#
#     def get_queryset(self):
#         year = int(self.kwargs['year'])
#         month = int(self.kwargs['month'])
#         article_list = Article.objects.filter(created_time__year=year, created_time__month=month)
#         for article in article_list:
#             article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
#         return article_list
#
#     def get_context_data(self, **kwargs):
#         kwargs['tag_list'] = Tag.objects.all().order_by('name')
#         return super(ArchiveView, self).get_context_data(**kwargs)
#

# 第五周新增 评论区域
# class CommentPostView(FormView):
#     form_class = BlogCommentForm
#     template_name = 'blog/detail.html'
#
#     def form_valid(self, form):
#         target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
#         comment = form.save(commit=False)
#         comment.article = target_article
#         comment.save()
#         self.success_url = target_article.get_absolute_url()
#         return HttpResponseRedirect(self.success_url)
#
#     def form_invalid(self, form):
#         target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])
#         return render(self.request, 'blog/detail.html', {
#             'form': form,
#             'article': target_article,
#             'comment_list': target_article.blogcomment_set.all(),
#         })
