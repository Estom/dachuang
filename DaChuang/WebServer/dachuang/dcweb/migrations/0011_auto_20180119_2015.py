# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-19 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcweb', '0010_auto_20180119_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernormal',
            name='desc',
            field=models.CharField(default='\u5c0f\u767d', max_length=300, verbose_name='\u7b80\u4ecb'),
        ),
        migrations.AlterField(
            model_name='usernormal',
            name='img',
            field=models.ImageField(default='1.jpg', null=True, upload_to='user', verbose_name='\u5934\u50cf'),
        ),
        migrations.AlterField(
            model_name='usernormal',
            name='phone',
            field=models.CharField(blank=True, default='11011011011', max_length=20, verbose_name='\u7535\u8bdd'),
        ),
    ]
