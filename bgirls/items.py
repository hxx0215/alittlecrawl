# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BgirlsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    detailURL = scrapy.Field()
    title = scrapy.Field()
    src = scrapy.Field()
    starcount = scrapy.Field()
    currentURL = scrapy.Field()
    _id = scrapy.Field()

    pass
