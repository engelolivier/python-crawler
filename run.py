#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/crawler" )

# from crawler import Crawler
from crawler import *

# On construit une liste d'url
crawler = CrawlerSiteMap("http://localhost:8000")
# Point de départ
crawler.crawl("http://localhost:8000/shop/")

# Construction du sitemap
# crawler.build_sitemap()