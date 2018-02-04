# -*- coding: utf-8 -*-

'''
力学与土木建筑 Mechanics,Civil Engineering and Architecture
'''

import scrapy
import sys
import os
import re
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin

class ArchitectureSpider(scrapy.Spider):
    name = 'Architecture'