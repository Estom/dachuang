# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-28 07:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcweb', '0011_auto_20180119_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='wechat_id',
            field=models.CharField(default='nothing', max_length=300, verbose_name='\u5fae\u4fe1\u53f7'),
        ),
    ]
