# -*- coding: utf-8 -*-

'''
动力与能源 Power and Energy
'''

import scrapy
import sys
import os
import re
from shoolnews.items import ShoolnewsItem
from urlparse import urljoin

class PowerandEnergySpider(scrapy.Spider):
    name = 'PowerandEnergy'