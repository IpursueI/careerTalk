# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CareertalkItem(scrapy.Item):
    sid = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()       # 宣讲会标题
    university = scrapy.Field()  # 学校名称
    issueTime = scrapy.Field()   # 宣讲会消息发布时间
    startTime = scrapy.Field()   # 宣讲会开始时间
    location = scrapy.Field()    # 宣讲会地点
    infoSource = scrapy.Field()  # 宣讲会信息来源
    infoDetailText = scrapy.Field()  #宣讲会详细信息(纯文本)
    infoDetailRaw = scrapy.Field()  #宣讲会原始详细信息(html)
    image_urls = scrapy.Field()
    images = scrapy.Field()

class CompanyItem(scrapy.Item):
    name = scrapy.Field()
    introduction = scrapy.Field()  #公司介绍
    
    phoneNumber = scrapy.Field()
    email = scrapy.Field()
    homePage = scrapy.Field()
    address = scrapy.Field()
    prop = scrapy.Field()        #公司性质
    scale = scrapy.Field()       #公司规模
    industry = scrapy.Field()    #公司性质
    
class NJUItem(CareertalkItem):   #南京大学
    company = scrapy.Field()

class NUAAItem(CareertalkItem):   #南京航空航天大学
    company = scrapy.Field()

class NJUSTItem(CareertalkItem):  #南京理工大学
    company = scrapy.Field()

class ZJGSUItem(CareertalkItem):  #浙江工商大学
    company = scrapy.Field()

class NJNUItem(CareertalkItem):   #南京师范大学
    company = scrapy.Field()

