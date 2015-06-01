#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

__author__ = 'phk'

import datetime
import time
import json
import re

from careerTalk.items import USSTItem, CompanyItem
import scrapy
from careerTalk.customUtil import CustomUtil, DoneSet
from pyquery import PyQuery as pq

chc = CustomUtil.convertHtmlContent
gfs = CustomUtil.getFirstStr


class USSTSpider(scrapy.Spider):
    name = "USST"
    allowed_domains = ["91.usst.edu.cn"]

    # 设置下载延时
    download_delay = 0.15

    # 可以通过该url获取到宣讲会的摘要数据,需要加入参数 【起始时间】
    start_urls = [
        "http://91.usst.edu.cn/meeting.asp?Tpage=1"
    ]
    home = "http://91.usst.edu.cn/"
    abs_url = "http://91.usst.edu.cn/meeting.asp?Tpage="

    def parse(self, response):
        # 解析当前页面
        for req in self.parse_items(response):
            yield req
        # 获取后续页面
        m = re.search(r'Page (\d+) of (\d+)', response.body)
        if m:
            curPage = int(m.group(1))
            totpage = int(m.group(2))
            if curPage == 1:
                for i in range(curPage+1, totpage+1):
                    url = self.abs_url+str(i)
                    yield scrapy.Request(url, callback=self.parse)

    def parse_items(self, response):
        links = response.css('a').extract()
        for link in links:
            a = pq(link)
            # http://91.usst.edu.cn/ActivityList.asp?ntype=%C6%F3%D2%B5%D5%D0%C6%B8&ctype=%D0%FB%BD%B2%BB%E1&TactiID=1356
            href = a.attr('href')
            m = re.search(r'&TactiID=(\d+)', href)
            if m:
                sid = m.group(1)
                title = a.text()

                url = self.home+href
                item = self.createItem(sid, title)
                if self.isNeedToParseDetail(url, item):
                    yield scrapy.Request(url, callback=self.parse_item_detail, meta={'item': item})

    def isNeedToParseDetail(self, url, item):
        # 要求ctype为双选会
        m = re.search(r'ctype=%D0%FB%BD%B2%BB%E1', url)
        return url and m and not DoneSet.isInDoneSet(self, item)

    def getDetailUrl(self, sid):
        return self.detail_url+"jobfair_"+sid+"_1.html"

    def parse_item_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        infos = response.css('td div::text').extract()

        startTime=None
        endTime=None
        location=None
        issueTime=None
        for info in infos:
            # 活动时间：2015-4-21 13:30—15:30
            info = info.strip()
            if info.__contains__(u'活动时间：'):
                startTime, endTime = CustomUtil.splitTimes(info.split(u'：')[1])
            # 活动地点：光电学院演讲厅
            elif info.__contains__(u'活动地点：'):
                location = info.split(u'：')[1]
            # 发布日期：2015-3-26 16:53:24
            elif info.__contains__(u'发布日期：'):
                issueTime = info.split(u'：')[1]
                issueTime = time.strptime(issueTime, CustomUtil.time_format+":%S")
                issueTime = time.strftime(CustomUtil.time_format, issueTime)

        item['startTime'] = startTime
        item['endTime'] = endTime
        item['location'] = location
        item['issueTime'] = issueTime

        infoDetailRaw = None
        ts = response.css('table table')[0]
        infoDetailRaw = chc(ts.css('tr:nth-child(5) td:nth-child(2)').extract())
        item['infoDetailRaw'] = infoDetailRaw
        return item

    @staticmethod
    def createItem(sid, title):
        item = USSTItem()
        item['sid'] = sid
        item['title'] = title
        return item