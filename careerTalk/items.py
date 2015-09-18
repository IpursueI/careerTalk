# -*- coding: utf-8 -*-
# coding=utf-8

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CareertalkItem(scrapy.Item):
<<<<<<< HEAD
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
=======
    university = scrapy.Field()  # 学校名称 中文全称
    title = scrapy.Field()       # 宣讲会标题
    issueTime = scrapy.Field()   # 宣讲会消息发布时间 2015-05-15
    startTime = scrapy.Field()   # 宣讲会开始时间  2015-05-15 18:30
    location = scrapy.Field()    # 宣讲会地点
    infoSource = scrapy.Field()  # 宣讲会信息来源
    infoDetailText = scrapy.Field()  # 宣讲会详细信息(纯文本)
    infoDetailRaw = scrapy.Field()  # 宣讲会原始详细信息(html)
    link = scrapy.Field()           # 宣讲会详细信息具体页面
    sid = scrapy.Field()        # 宣讲会源id

>>>>>>> dev-phk

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
<<<<<<< HEAD
    
=======

    def __init__(self, name, intro=None, phone=None, email=None, homePage=None, addr=None, prop=None, scale=None, industry=None):
        super(CompanyItem, self).__init__()
        self['name'] = name
        if intro:
            self['introduction'] = intro
        if phone:
            self['phoneNumber'] = phone
        if email:
            self['email'] = email
        if homePage:
            self['homePage'] = homePage
        if addr:
            self['address'] = addr
        if prop:
            self['prop'] = prop
        if scale:
            self['scale'] = scale
        if industry:
            self['industry'] = industry


# 东南大学
class SEUItem(CareertalkItem):
    kind = scrapy.Field()        # 宣讲会类型，这里按地点分类
    endTime = scrapy.Field()

    targetAcademic = scrapy.Field()    # 目标学历
    targetMajor = scrapy.Field()    # 目标专业

    def __init__(self):
        super(SEUItem, self).__init__()
        self['university'] = u'东南大学'
        self['infoSource'] = u'东南大学就业信息网'


# 北京航空航天大学
class BUAAItem(CareertalkItem):
    company = scrapy.Field()

    endTime = scrapy.Field()

    def __init__(self):
        super(BUAAItem, self).__init__()
        self['university'] = u'北京航空航天大学'
        self['infoSource'] = u'北京航空航天大学就业信息网'


# 北京理工大学
class BITItem(CareertalkItem):
    company = scrapy.Field()

    endTime = scrapy.Field()

    def __init__(self):
        super(BITItem, self).__init__()
        self['university'] = u'北京理工大学'
        self['infoSource'] = u'北京理工大学就业信息网'


# 中国人民大学
class RUCItem(CareertalkItem):
    company = scrapy.Field()

    remark = scrapy.Field()

    def __init__(self):
        super(RUCItem, self).__init__()
        self['university'] = u'中国人民大学'
        self['infoSource'] = u'中国人民大学就业指导中心'


# 清华大学
class THItem(CareertalkItem):
    company = scrapy.Field()

    endTime = scrapy.Field()

    def __init__(self):
        super(THItem, self).__init__()
        self['university'] = u'清华大学'
        self['infoSource'] = u'清华大学学生职业发展指导中心'


# 北京大学
class PKUItem(CareertalkItem):
    company = scrapy.Field()

    endTime = scrapy.Field()

    def __init__(self):
        super(PKUItem, self).__init__()
        self['university'] = u'北京大学'
        self['infoSource'] = u'北京大学学生就业指导服务中心'


# 上海理工大学
class USSTItem(CareertalkItem):
    company = scrapy.Field()

    endTime = scrapy.Field()

    def __init__(self):
        super(USSTItem, self).__init__()
        self['university'] = u'上海理工大学'
        self['infoSource'] = u'上海理工大学就业信息服务网'


# 华东理工大学
class ECUSTItem(CareertalkItem):
    company = scrapy.Field()

    endTime = scrapy.Field()
    targetAcademic = scrapy.Field()    # 目标学历
    targetMajor = scrapy.Field()    # 目标专业

    def __init__(self):
        super(ECUSTItem, self).__init__()
        self['university'] = u'华东理工大学'
        self['infoSource'] = u'华东理工大学就业信息网'


# 上海交通大学
class SJTUItem(CareertalkItem):
    company = scrapy.Field()

    endTime = scrapy.Field()

    def __init__(self):
        super(SJTUItem, self).__init__()
        self['university'] = u'上海交通大学'
        self['infoSource'] = u'上海交通大学招聘信息服务网'


>>>>>>> dev-phk
class NJUItem(CareertalkItem):   #南京大学
    company = scrapy.Field()

<<<<<<< HEAD
class NUAAItem(CareertalkItem):   #南京航空航天大学
    company = scrapy.Field()

class NJUSTItem(CareertalkItem):  #南京理工大学
    company = scrapy.Field()

class ZJGSUItem(CareertalkItem):  #浙江工商大学
    company = scrapy.Field()

class NJNUItem(CareertalkItem):   #南京师范大学
    company = scrapy.Field()

class HHUItem(CareertalkItem):    #河海大学
    company = scrapy.Field()

class CAAItem(CareertalkItem):  #中国美术学院
    company = scrapy.Field()

class CJLUItem(CareertalkItem):  #中国计量学院
    company = scrapy.Field()

class ZJUTItem(CareertalkItem):  #浙江工业大学
    company = scrapy.Field()

class HZNUItem(CareertalkItem):  #杭州师范大学
    company = scrapy.Field()

class ZJUItem(CareertalkItem):  #浙江大学
    company = scrapy.Field()

class NJAUItem(CareertalkItem):  #南京农业大学
    company = scrapy.Field()
=======
    def __init__(self):
        super(NJUItem, self).__init__()
        self['university'] = u'南京大学'
        self['infoSource'] = u'南京大学就业创业信息网'
>>>>>>> dev-phk
