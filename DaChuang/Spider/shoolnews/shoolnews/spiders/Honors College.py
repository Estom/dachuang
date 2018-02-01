# -*- coding: utf-8 -*-

'''
教育实验学院 Honors College
'''

import scrapy
import sys
import os
import re
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin

class HonorsCollegeSpider(scrapy.Spider):
    name = 'HonorsCollege'
