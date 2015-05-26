#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

__author__ = 'phk'

import re
import json

import scrapy
from careerTalk import items
from careerTalk.customUtil import CustomUtil, DoneSet
from pyquery import PyQuery as pq

chc = CustomUtil.convertHtmlContent
gfs = CustomUtil.getFirstStr


class BITSpider(scrapy.Spider):
    name = "BIT"
    allowed_domains = ["job.bit.edu.cn"]

    # 可以通过该url直接获取到所有的数据,按照第一个字段（具体item的url，只有id不同）降序排列
    # iDisplayStart表示开始的item数量而非页数
    inf_num = '3000000'
    start_urls = [
        "http://job.bit.edu.cn/employment-activities.html?ajax=getEventList&sSortDir_0=desc&iDisplayStart=0&iDisplayLength="+inf_num
    ]
    home = 'http://job.bit.edu.cn/'
    # 具体页面的链接 需要添加参数tx_extevent_pi1[uid]=758
    detail_url= 'http://job.bit.edu.cn/employment-activities.html?tx_extevent_pi1[cmd]=preview&tx_extevent_pi1[uid]='

    def parse(self, response):
        return self.parse_items(response)
        # 并不需要解析下一个页面，因为当前页面以及获取的所有需要的摘要信息

    def parse_items(self, response):
        jdata = json.loads(response.body)
        datas = jdata['aaData']
        for data in datas:
            a = pq(data[0])
            url = self.home+a.attr('href')
            title = a.text()
            location = data[1]
            ts = CustomUtil.get_times(data[2])
            startTime = None
            endTime = None
            if len(ts) >= 1:
                startTime = ts[0]
            if len(ts) >= 2:
                endTime = ts[1]
            m = re.search(r'tx_extevent_pi1%5Buid%5D=(\d+)', url)
            sid = None
            if m:
                sid = m.group(1)
            item = self.createItem(sid, title, startTime, endTime, location)
            if self.isNeedToParseDetail(url, item):
                yield scrapy.Request(url, callback=self.parse_item_detail, meta={'item': item})

    def isNeedToParseDetail(self, url, item):
        return url and not DoneSet.isInDoneSet(self, item)

    def parse_item_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        infoDetailRaw = response.css('.event_content').extract()

        # 提取发布时间 发布时间: 2015-05-12 10:00
        pattern = '发布时间: '+'('+CustomUtil.time_pattern+')'
        m = re.search(pattern, response.body)
        issueTime = None
        if m:
            issueTime = m.group(1)

        item['infoDetailRaw'] = chc(infoDetailRaw)
        item['issueTime'] = issueTime

        # 因为公司数据不规则，无法直接提取公司信息
        return item

    @staticmethod
    def createItem(sid, title, startTime, endTime, location):
        item = items.BUAAItem()
        item['sid'] = sid
        item['title'] = title
        item['startTime'] = startTime
        item['endTime'] = endTime
        item['location'] = location
        return item

    """
    主页面返回数据
    {
        "sEcho": null,
        "iTotalRecords": 676,
        "iTotalDisplayRecords": 676,
        "aaData": [
                    [
                    "<a href=\"employment-activities.html?tx_extevent_pi1%5Bcmd%5D=preview&amp;tx_extevent_pi1%5Buid%5D=758\" target=\"target\" >京东方暑期实习生招聘</a>",
                    "唯实报告厅",
                    "2015-05-27 14:30 <br /> 2015-05-27 16:30",
                    "300"
                    ],
                    [
                    "<a href=\"employment-activities.html?tx_extevent_pi1%5Bcmd%5D=preview&amp;tx_extevent_pi1%5Buid%5D=757\" target=\"target\" >全球500强 罗氏诊断 实习生招聘宣讲会</a>",
                    "研究生楼208",
                    "2015-05-18 19:00 <br /> 2015-05-18 21:00",
                    "359"
                    ]
                   ]
    }
    """
