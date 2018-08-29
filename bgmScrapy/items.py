# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BgmscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BangumiItem(scrapy.Item):
    ranking = scrapy.Field()
    name = scrapy.Field()
    episodes = scrapy.Field()
    time = scrapy.Field()
    staffs = scrapy.Field()
    score = scrapy.Field()
    voteNum = scrapy.Field()
