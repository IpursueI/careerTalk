# -*- coding: utf-8 -*-
# coding=utf-8

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CareertalkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BaseItem(scrapy.Item):
    university = scrapy.Field()  # 学校名称 中文全称
    title = scrapy.Field()       # 宣讲会标题
    issueTime = scrapy.Field()   # 宣讲会消息发布时间 2015-05-15
    startTime = scrapy.Field()   # 宣讲会开始时间  2015-05-15 18:30
    location = scrapy.Field()    # 宣讲会地点
    infoSource = scrapy.Field()  # 宣讲会信息来源


# 东南大学
class SEUItem(BaseItem):
    kind = scrapy.Field()        # 宣讲会类型，这里按地点分类
    link = scrapy.Field()        # 相关连接
    sid = scrapy.Field()        # 宣讲会id
    infoDetail = scrapy.Field()  # 详细信息
    startTime_date = scrapy.Field()   # 宣讲日期
    startTime_time = scrapy.Field()   # 宣讲时间
    sponsor = scrapy.Field()     # 主办方
    absLink = scrapy.Field()     # 摘要页面的连接

    targetAcademic = scrapy.Field()    # 目标学历
    targetMajor = scrapy.Field()    # 目标专业


# 北京航空航天大学
class BUAAItem(BaseItem):
    endTime = scrapy.Field()



class NJUItem(BaseItem):   #南京大学
    infoDetail = scrapy.Field()  #宣讲会详细信息
