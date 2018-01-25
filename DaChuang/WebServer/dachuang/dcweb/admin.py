# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from dcweb.models import Article, Category, Tag, Source, Publisher,UserNormal,Recommend,Star,History
#from dcweb.models import UserProfile

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')
    ordering = ('-number',)

admin.site.register(Category,CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name','number')
    ordering = ('-number',)

admin.site.register(Tag, TagAdmin)


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Source,SourceAdmin)


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name','source',)
admin.site.register(Publisher,PublisherAdmin)


class RecommendAdmin(admin.ModelAdmin):
    list_display = ('id','user','article')

admin.site.register(Recommend,RecommendAdmin)


class StarAdmin(admin.ModelAdmin):
    list_display = ('id','user','publisher')

admin.site.register(Star,StarAdmin)


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id','user','article','time')
    ordering = ('-time',)
admin.site.register(History,HistoryAdmin)
# fieldsets 用来显示详细页的字段集合
# fieldsets = (
#         ['Main',{
#             'fields':('name','email'),
#         }],
#         ['Advance',{
#             'classes': ('collapse',), # CSS
#             'fields': ('age',),
#         }]
#     )
# fields 用来显示不同的字段
# fields = ('name', 'email')
# inlines 用来定义是否显示外键的关联列表
# inlines = [TagInline]
# class TagInline(admin.TabularInline):
#     model = Tag
# list_distplay 定义列表页的字段
# search_fields 定义可搜索的名字


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'date_publish', 'category')
    search_fields = ('title','publisher')
    ordering = ('-date_publish',)

admin.site.register(Article,ArticleAdmin)

class UserNormalInline(admin.StackedInline):
    model = UserNormal
    can_delete = False
    verbose_name = u'用户详细信息'

class UserAdmin(UserAdmin):
    list = []
    list.append(UserNormalInline)
    inlines = list

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# class UserNormalAdmin(admin.ModelAdmin):
#     list_display = ('user', 'name', 'get_email', 'get_is_active')  # 定义admin总览里每行的显示信息，由于email是在userprofile的外键user表中，所以需要特殊返回，注意这个字段不能用user__email的形式
#     search_fields = ('user__username', 'name')  # 定义搜索框以哪些字段可以搜索，因为username是在user表中，所以用user__username的形式，这里需要注意下，不能直接用user表名，要用字段名，表名__字段名
#     list_filter = ('user__groups', 'user__is_active')  #传入的需要是列表，设定过滤列表
#
#     def get_email(self, obj):  # 定义这个函数是由于email是在userprofile表的外键表user里，所以需要单独return一下
#         return obj.user.email
#     get_email.short_description = 'Email'  #list展示时候显示的title
#     get_email.admin_order_field = 'user__email'  #指定排序字段
#
#     def get_is_active(self, obj):
#         return obj.user.is_active
#     get_is_active.short_description = '有效'
#     get_is_active.admin_order_field = 'user__is_active'

# 引用的固定格式，注册的model和对应的Admin，Admin放在后边，同样还有noregister方法：比如admin.site.noregister(Group)，把group这个表在admin中去掉（默认user和group都是注册到admin中的）
#admin.site.register(UserProfile, UserProfileAdmin)
# class DirectionAdmin(admin.ModelAdmin):
#     list_display = ('describe', 'db_name')
#
#     class Media:
#         js = ('static/blog/js/jquery.js',)
#         css = {
#              'all': ('static/lib/css/bootstrap.css',)
#         }
# admin.site.register(UserProfileAdmin,DirectionAdmin)