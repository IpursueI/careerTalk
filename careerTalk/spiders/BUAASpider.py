#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

__author__ = 'phk'

import scrapy
from careerTalk import items
import re
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent
gfs = CustomUtil.getFirstStr


class BUAASpider(scrapy.Spider):
    name = "BUAA"
    university = u'北京航空航天大学'
    infoSource = u'北京航空航天大学就业信息网'
    allowed_domains = ["career.buaa.edu.cn"]
    start_urls = [
        "http://career.buaa.edu.cn/getJobfairAllInfoAction.dhtml?more=all&selectedNavigationName=RecruitmentInfoMain&selectedItem=jobFair&pageIndex=1"
    ]
    # 摘要页面的链接，需要添加参数pageIndex=2
    abs_page_url = "http://career.buaa.edu.cn/getJobfairAllInfoAction.dhtml?more=all&selectedNavigationName=RecruitmentInfoMain&selectedItem=jobFair"
    # 具体页面的链接 需要添加参数id=c8f7314d-b2b1-4943-9f48-917bd552f06b&
    detail_url= 'http://career.buaa.edu.cn/calEmpDetailAction.dhtml?tabletype=careerTalk&selectedItem=jobFair&more=all&selectedNavigationName=RecruitmentInfoMain'
    # 将正则表达式编译成Pattern对象
    link_pattern = re.compile(r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')

    def createItem(self, title, startTime, endTime, location, issueTime):
        item = items.BUAAItem()
        item['university'] = BUAASpider.university
        item['infoSource'] = BUAASpider.infoSource
        item['title'] = title
        item['startTime'] = startTime
        item['endTime'] = endTime
        item['location'] = location
        item['issueTime'] = issueTime
        return item

    def parse(self, response):
        items = self.parse_items(response)
        self.parse_next_pages(response)
        return items

    def parse_items(self, response):
        trs = response.css('.info_table tr')
        for tr in trs:
            title = tr.css(".info_left a::text").extract()
            sTime = tr.css('.csstime::text').extract()
            location = tr.css('.cssadress::text').extract()
            issueTime = tr.css('.info_right font ::text').extract()

            # 提取地点
            # 地点：如心会议中心大报告厅 --> 提取关键字
            location = chc(location)
            m = re.search(ur'地点：(.*)', gfs(location))
            if m:
                location = m.group(1)
            # 提取开始时间
            startTime = None
            endTime = None
            # 时间：2015-03-27 14:00 至 2015-03-27 18:00
            ts = CustomUtil.get_times(gfs(sTime))
            if len(ts) == 2:
                startTime = ts[0]
                endTime = ts[1]

            # 提取发布时间
            issueTime = chc(issueTime)
            ts = CustomUtil.get_date(gfs(issueTime))
            if len(ts):
                issueTime = ts[0]

            yield self.createItem(chc(title), startTime, endTime, location, issueTime)

    def parse_next_pages(self, response):
        pass
        # total_page = response.css('#\“total_page\”::text').extract()
        # print 'totpage:', total_page