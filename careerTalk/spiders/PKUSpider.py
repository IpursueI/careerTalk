#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

__author__ = 'phk'

import datetime
import time
import json
import re

from careerTalk.items import PKUItem, CompanyItem
import scrapy
from careerTalk.customUtil import CustomUtil, DoneSet

chc = CustomUtil.convertHtmlContent
gfs = CustomUtil.getFirstStr


class PKUSpider(scrapy.Spider):
    name = "PKU"
    allowed_domains = ["scc.pku.edu.cn"]

    # 设置下载延时
    download_delay = 0.15
    # 从上个月开始
    delta = datetime.timedelta(days=-30)
    today = datetime.datetime.today()+delta
    strT = today.strftime("%Y-%m-%d %H:%M")
    # 可以通过该url获取到宣讲会的摘要数据,需要加入参数 【起始时间】
    start_urls = [
        # http://scc.pku.edu.cn/home!findJobFairs?fairDate=2015-01-06 00:00
        "http://scc.pku.edu.cn/home!findJobFairs?fairDate="+strT
    ]
    abs_url = "http://scc.pku.edu.cn/home!findJobFairs?fairDate=";

    # 具体页面的链接
    # http://scc.pku.edu.cn/jobfair_ff8080814c03f58e014c06e8a3d40113_1.html
    detail_url = "http://scc.pku.edu.cn/"

    def parse(self, response):
        return self.parse_items(response)
        # 并不需要解析下一个页面，start_urls包含了所有要解析的数据

    def parse_items(self, response):
        # 返回的是json数据
        body = response.body
        jdatas = json.loads(body)['data']
        # 默认返回10个数据,记录最后一个数据的时间，作为获取下一个页面的参数
        fairDate = None
        for data in jdatas:
            # print fairDate
            print data['title'],data['fairDate']
            fairDate = data.get('fairDate', fairDate)
            # {"id":"ff8080814a7d39f9014acc5939e1005f","title":"江苏省关于2015年应届优秀大学毕业生选调工作的通知 ","fairDate":"2015-01-13 16:30","startTime":"16:30","endTime":"18:30","startDay":"01月13日","lastUpdate":"2015年01月09日","fairCategory":"jobfair","isStatic":1,"location":"新太阳学生中心212室"}
            # 如果是宣讲会类型
            if data.get('fairCategory') == 'jobfair':
                sid = data.get('id')
                title = data.get('title')
                location = data.get('location')
                startTime = data.get('fairDate')
                endTime = None
                if data.get('endTime'):
                    endTime = startTime.split(' ')[0]+' '+data['endTime']
                item = self.createItem(sid, title, startTime, endTime, location)
                url = self.getDetailUrl(sid)

                if self.isNeedToParseDetail(url, item):
                    yield scrapy.Request(url, callback=self.parse_item_detail, meta={'item': item})
        if fairDate:
            url = self.abs_url+fairDate
            yield scrapy.Request(url, callback=self.parse)

    def isNeedToParseDetail(self, url, item):
        return url and not DoneSet.isInDoneSet(self, item)

    def getDetailUrl(self, sid):
        return self.detail_url+"jobfair_"+sid+"_1.html"

    def parse_item_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        infoDetailRaw = response.css('.articleContext').extract()

        item['infoDetailRaw'] = chc(infoDetailRaw)
        return item

    @staticmethod
    def createItem(sid, title, startTime, endTime, location):
        item = PKUItem()
        item['sid'] = sid
        item['title'] = title
        item['startTime'] = startTime
        item['endTime'] = endTime
        item['location'] = location
        return item