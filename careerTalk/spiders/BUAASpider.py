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
    name = "BUAA"
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

    def parse(self, response):
        items = self.parse_items(response)
        for item in items:
            yield  item

        urls = self.parse_next_pages(response)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse_items(self, response):
        # print 'parse: '+response.url
        trs = response.css('.info_table tr')
        for tr in trs:
            title = tr.css(".info_left a::text").extract()
            sTime = tr.css('.csstime::text').extract()
            location = tr.css('.cssadress::text').extract()
            issueTime = tr.css('.info_right font ::text').extract()
            tid = tr.css('.info_left a').re(BUAASpider.link_pattern)
            tableType = tr.css('.info_left a').re(r'tabletype=careerTalk')

            # 若url包含tabletype=careerTalk，则表示该item为宣讲会类型
            # item中可能包含其他类型的，比如tabletype=jobFair，为双选会，这些直接跳过即可
            if len(tableType)==0:
                continue

            # 提取id
            tid = chc(tid)

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

            item = self.createItem(tid, chc(title), startTime, endTime, location, issueTime)
            url = self.getDetailUrlById(tid)
            if self.isNeedToParseDetail(url, item):
                yield scrapy.Request(url, callback=self.parse_item_detail, meta={'item': item})

    def isNeedToParseDetail(self, url, item):
        return url and not DoneSet.isInDoneSet(self, item)

    def parse_item_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        infoDetailRaw = response.css('.left_content').extract()

        # 提取公司信息
        cintro = response.css('.article_content .unit_content').extract()
        cintro = CustomUtil.h2t(chc(cintro))

        org_info_tds = response.css('.child_title td').extract()
        contact_info = response.css('.contact_information td').extract()
        infos = []
        for td in org_info_tds:
            t = pq(td).text()
            infos.append(t)
        for td in contact_info:
            t = pq(td).text()
            infos.append(t)
        info_dic = {}
        dkey = None
        for i in range(len(infos)):
            if i&1:
                if dkey:
                    info_dic[dkey] = infos[i].strip()
            else:
                dkey = infos[i].strip()
        # for key in info_dic:
        #     print key,info_dic[key]
        cname = info_dic.get(u'公司名称：')
        cpro = info_dic.get(u'公司性质：')
        cscale = info_dic.get(u'公司规模：')
        cind = info_dic.get(u'公司行业：')
        cphone = info_dic.get(u'联系电话：')
        chome = info_dic.get(u'公司主页：')
        cemail = info_dic.get(u'招聘邮箱：')
        caddr = info_dic.get(u'公司地址：')

        company = items.CompanyItem(cname,
                                    intro=cintro,
                                    prop=cpro,
                                    scale=cscale,
                                    phone=cphone,
                                    homePage=chome,
                                    industry=cind,
                                    email=cemail,
                                    addr=caddr)
        item['company'] = company
        item['infoDetailRaw'] = chc(infoDetailRaw)
        return item

    def parse_next_pages(self, response):
        m = re.search('totalpage: (\d+)', response.body)
        if m:
            total_page = int(m.group(1))
            for i in range(1, total_page):
                yield self.getAbsUrlsByPage(i)

    @classmethod
    def getDetailUrlById(cls, tid):
        return cls.detail_url+"&id="+tid

    @classmethod
    def getAbsUrlsByPage(cls, page):
        return cls.abs_page_url+"&pageIndex=%d" % page

    @staticmethod
    def createItem(sid, title, startTime, endTime, location, issueTime):
        item = items.BUAAItem()
        item['sid'] = sid
        item['title'] = title
        item['startTime'] = startTime
        item['endTime'] = endTime
        item['location'] = location
        item['issueTime'] = issueTime
        return item

