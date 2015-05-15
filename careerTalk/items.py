# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CareertalkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NJUItem(scrapy.Item):      #南京大学
    university = scrapy.Field()  #学校名称
    issueTime = scrapy.Field()   #宣讲会消息发布时间
    startTime = scrapy.Field()   #宣讲会开始时间
    location = scrapy.Field()    #宣讲会地点
    infoSource = scrapy.Field()  #宣讲会信息来源
    infoDetail = scrapy.Field()  #宣讲会详细信息
