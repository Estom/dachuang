# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-19 03:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcweb', '0006_remove_usernormal_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernormal',
            name='sex',
            field=models.IntegerField(blank=True, choices=[(0, '\u7537'), (1, '\u5973')], default=0, verbose_name='\u6027\u522b'),
        ),
    ]
