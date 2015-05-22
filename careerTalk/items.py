# -*- coding: utf-8 -*-
# coding=utf-8

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CareertalkItem(scrapy.Item):
    university = scrapy.Field()  # 学校名称 中文全称
    title = scrapy.Field()       # 宣讲会标题
    issueTime = scrapy.Field()   # 宣讲会消息发布时间 2015-05-15
    startTime = scrapy.Field()   # 宣讲会开始时间  2015-05-15 18:30
    location = scrapy.Field()    # 宣讲会地点
    infoSource = scrapy.Field()  # 宣讲会信息来源
    infoDetailText = scrapy.Field()  #宣讲会详细信息(纯文本)
    infoDetailRaw = scrapy.Field()  #宣讲会原始详细信息(html)


class CompanyItem(scrapy.Item):
    # 关键字段
    name = scrapy.Field()
    introduction = scrapy.Field()  #公司介绍

    # 其余字段
    phoneNumber = scrapy.Field()
    email = scrapy.Field()
    homePage = scrapy.Field()
    address = scrapy.Field()
    prop = scrapy.Field()        #公司性质
    scale = scrapy.Field()       #公司规模
    industry = scrapy.Field()    #公司性质


# 东南大学
class SEUItem(CareertalkItem):
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
class BUAAItem(CareertalkItem):
    company = scrapy.Field()

    endTime = scrapy.Field()



class NJUItem(CareertalkItem):   #南京大学
    university = scrapy.Field()  #宣讲会详细信息
    company = scrapy.Field()
