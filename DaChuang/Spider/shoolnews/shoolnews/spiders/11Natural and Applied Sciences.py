# -*- coding: utf-8 -*-

'''
理学院 school of Natural and Applied Sciences
'''

import scrapy
import sys
import os
import re
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin

class NaturalandAppliedSciencesSpider(scrapy.Spider):
    name = 'NaturalandAppliedSciences'
