#!/usr/bin/python
# -*- coding: utf-8 -*-

import feedparser

# Init Parse RSS
def getRSS():
    # URL RSS
    urlRss = 'http://ep00.epimg.net/rss/tecnologia/portada.xml'
    #feed = feedparser.parse('http://ep00.epimg.net/rss/tecnologia/portada.xml')

    # Parse RSS
    feed = feedparser.parse( urlRss )
    return feed
