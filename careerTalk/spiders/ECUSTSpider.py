#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

__author__ = 'phk'

import scrapy
from careerTalk import items
import re
from careerTalk.customUtil import CustomUtil,DoneSet
from pyquery import PyQuery as pq
chc = CustomUtil.convertHtmlContent
gfs = CustomUtil.getFirstStr


class BUAASpider(scrapy.Spider):
    name = "ECUST"
    allowed_domains = ["career.ecust.edu.cn"]
    start_urls = [
        "http://career.ecust.edu.cn/jsp/huali_lecture_achieve_start.jsp?page=1",
        "http://career.ecust.edu.cn/jsp/huali_lecture_achieve_end.jsp?page=1"
    ]
    #
    # 具体页面的链接 需要添加参数zphbh=abdf5277-fdcd-11e4-ad18-c38ef4511bf5
    detail_url = 'http://career.ecust.edu.cn/jsp/huali_lecture_achieve_detail.jsp?zphbh='
    # 将正则表达式编译成Pattern对象
    link_pattern = re.compile(r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')

    def parse(self, response):
        items = self.parse_items(response)
        for item in items:
            yield item

        urls = self.parse_next_pages(response)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse_items(self, response):
        # print 'parse: '+response.url
        trs = response.css('.list_main_content tr')
        for tr in trs:
            tds = tr.css('td')
            if len(tds) >= 4:
                a = chc(tds[0].css('a').extract())
                a = pq(a)
                title = a.text()

                tdt = pq(tds[1].extract()).text().strip()
                location = pq(tds[2].extract()).text().strip()
                date = pq(tds[3].extract()).text().strip()

                startTime = date+" "+tdt
                startTime = CustomUtil.formatTime(startTime)

                sid = None
                url = None
                m = re.search(self.link_pattern, a.attr('href'))
                if m:
                    sid = m.group()
                    url = self.detail_url+sid
                    item = self.createItem(sid, title, startTime, None, location, None)
                    if self.isNeedToParseDetail(url, item):
                        yield scrapy.Request(url, callback=self.parse_item_detail, meta={'item': item})

    def isNeedToParseDetail(self, url, item):
        return url and not DoneSet.isInDoneSet(self, item)

    def parse_item_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        trs = response.css('.detail_content_display tr')

        if len(trs) >= 6:
            # 目标学历
            targetAcademic = CustomUtil.strip(chc(trs[1].css('td:nth-child(4)::text').extract()))
            # 目标专业
            targetMajor = CustomUtil.strip(chc(trs[2].css('td:nth-child(2)::text').extract()))

            # 公司名
            cname = CustomUtil.strip(chc(trs[0].css('td:nth-child(2)::text').extract()))
            # 公司简介
            cintro = CustomUtil.strip(chc(trs[3].css('td:nth-child(2)::text').extract()))

            # 招聘简章
            infoDetailRaw = trs[4].css('td:nth-child(2)').extract()

            company = items.CompanyItem(cname,
                                        intro=cintro)
            item['targetAcademic'] = targetAcademic
            item['targetMajor'] = targetMajor
            item['company'] = company
            item['infoDetailRaw'] = chc(infoDetailRaw)
            return item

    def parse_next_pages(self, response):
        url = response.url.split('?')[0]
        a = chc(response.css('.nextpage a').extract())
        if a:
            a = pq(a)
            m = re.search(r'page=(\d+)', a.attr('href'))
            if m:
                nextP = int(m.group(1))
                yield url+'?page=%d' % nextP

    @staticmethod
    def createItem(sid, title, startTime, endTime, location, issueTime):
        item = items.ECUSTItem()
        item['sid'] = sid
        item['title'] = title
        item['startTime'] = startTime
        item['endTime'] = endTime
        item['location'] = location
        item['issueTime'] = issueTime
        return item