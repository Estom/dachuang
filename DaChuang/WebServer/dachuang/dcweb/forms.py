# -*- coding:utf-8 -*-
from django import forms
from django.conf import settings
from django.db.models import Q
from models import User
import re
from models import UserNormal
# 通过django定义的表单，统一前端和后台数据表达的方式，可以一次性完成验证数据、装载数据等操作
class LoginForm(forms.Form):
    '''
    登录Form
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required","class":"form-control",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required","class":"form-control",}),
                              max_length=20,error_messages={"required": "password不能为空",})

class RegForm(forms.Form):
    '''
    注册表单
    '''
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required","class":"form-control",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required","class":"form-control",}),
                              max_length=50,error_messages={"required": "email不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required","class":"form-control",}),
                              max_length=20,min_length=6,error_messages={"required": "password不能为空",})


class PersonForm(forms.Form):
    '''
    评论表单
    '''
    sex = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": u"性别","id": "sex", "required": "required","tabindex": "1","class":"form-control",}),
                              error_messages={"required":"sex不能为空",},
                          label=u'性别',required=False)
    age = forms.IntegerField(widget=forms.TextInput(attrs={"placeholder": u"年龄","id":"age",
                                                           "required":"required", "tabindex":"2","class":"form-control",}),
                                 error_messages={"required":"age不能为空",},
                           label=u'年龄',required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": u"电话","id":"phone","tabindex":"3","class":"form-control",}),
                              max_length=100, required=False,label=u'电话')
    desc = forms.CharField(widget=forms.Textarea(attrs={"placeholder": u"签名","id":"desc","required": "required", "cols": "80",
                                                           "rows": "5", "tabindex": "4","class":"form-control",}),
                                                    error_messages={"required":"评论不能为空",},
                           label=u'签名',required=False)
    img = forms.ImageField(label=u'头像', required=True)

class PersonsForm(forms.ModelForm):
    class Meta:
        model = UserNormal
        fields = [ 'age','sex','phone','desc','img']