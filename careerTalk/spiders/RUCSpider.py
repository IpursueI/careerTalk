#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

__author__ = 'phk'

import re
import time

import scrapy
from careerTalk.items import RUCItem
from careerTalk.customUtil import CustomUtil, DoneSet
from pyquery import PyQuery as pq

chc = CustomUtil.convertHtmlContent
gfs = CustomUtil.getFirstStr


class RUCSpider(scrapy.Spider):
    name = "RUC"
    allowed_domains = ["career.ruc.edu.cn"]

    # 设置下载延时
    download_delay = 0.5

    # 可以通过该url直接获取到所有的数据,但数据是按id排列，而id与创建时间之间的关系并不明确
    start_urls = [
        "http://career.ruc.edu.cn/news.asp"
    ]
    home = 'http://career.ruc.edu.cn/'
    # 具体页面的链接 需要添加参数id=1
    detail_url = "http://career.ruc.edu.cn/article_show2.asp?id="

    def parse(self, response):
        return self.parse_items(response)
        # 并不需要解析下一个页面，因为当前页面以及获取的所有需要的摘要信息

    def parse_items(self, response):
        # <a href="article_show2.asp?id=2648" target="_blank" class="STYLE14"><font face="幼圆" color="black">国家电网鲁能集团</font></a>
        links = response.css('a')
        for link in links:
            a = pq(link.extract())
            url = self.home+a.attr('href')
            m = re.search(r'article_show2.asp\?id=(\d+)', url)
            if m:
                sid = m.group(1)
                title = a.text()
                item = self.createItem(sid, title)
                if self.isNeedToParseDetail(url, item):
                    yield scrapy.Request(url, callback=self.parse_item_detail, meta={'item': item})

    def isNeedToParseDetail(self, url, item):
        return url and not DoneSet.isInDoneSet(self, item)

    def parse_item_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        infoDetailRaw = response.css('.STYLE15').extract()

        infos = response.css('.STYLE13').extract()
        location = None
        remark = None
        startTime = None
        if len(infos) >= 3:
            texts = [pq(infos[i]).text() for i in range(3)]
            # 时间：  2014/11/15 09:30
            m = re.search(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}', texts[0])
            if m:
                startTime = m.group()
                startTime = time.strptime(startTime, "%Y/%m/%d %H:%M")
                startTime = time.strftime(CustomUtil.time_format, startTime)
            # 地点：  世纪馆
            m = re.search(ur'地点：(.*)', texts[1], re.X)
            if m:
                location = m.group(1).strip()
            # 备注（要求）：  宣讲后会有面试，请同学们踊跃参加！
            m = re.search(ur'备注（要求）：(.*)', texts[2], re.X)
            if m:
                remark = m.group(1).strip()
        item['location'] = location
        item['remark'] = remark
        item['startTime'] = startTime

        item['infoDetailRaw'] = chc(infoDetailRaw)
        # 因为公司数据不规则，无法直接提取公司信息
        return item

    @staticmethod
    def createItem(sid, title):
        item = RUCItem()
        item['sid'] = sid
        item['title'] = title
        return item