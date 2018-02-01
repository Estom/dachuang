# -*- coding: utf-8 -*-

'''
软件与微电子 Software and Microelectronics
'''

import scrapy
import sys
import os
import re
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin

class SoftwareSpider(scrapy.Spider):
    name = 'Software'