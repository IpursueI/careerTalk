#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

__author__ = 'phk'


import scrapy
from careerTalk.items import SJTUItem, CompanyItem
import re
from careerTalk.customUtil import CustomUtil, DoneSet
from pyquery import PyQuery as pq
chc = CustomUtil.convertHtmlContent
gfs = CustomUtil.getFirstStr


class SJTUSpider(scrapy.Spider):
    name = "SJTU"
    allowed_domains = ["www.job.sjtu.edu.cn"]
    start_urls = [
        # 已举办的宣讲会
        "http://www.job.sjtu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=searchXjhxx&xjhType=yjb&resetPageSize=100000&pageMethod=next&currentPage=0",
        # 所有（未举办的）宣讲会 todo 未经测试
        "http://www.job.sjtu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=searchXjhxx&xjhType=all&resetPageSize=100000&pageMethod=next&currentPage=0"
    ]
    # 具体页面的链接 需要添加参数id=7fhbmvMq4iKZiniEiG4cod
    detail_url="http://www.job.sjtu.edu.cn/eweb/jygl/zpfw.so?modcode=jygl_xjhxxck&subsyscode=zpfw&type=viewXjhxx"
    # 将正则表达式编译成Pattern对象
    id_pattern = re.compile(r"viewXphxx\('(\w{22})'\)")

    def parse(self, response):
        items = self.parse_items(response)
        for item in items:
            yield item

        # 第一个页面设置了pageSize=100000，所以应该包含了所有需要的数据，开发的时候只有500多数据

    def parse_items(self, response):
        # print 'parse: '+response.url
        trs = response.css('.z_newsl li')
        for tr in trs:
            divs = tr.css('div')
            if len(divs) >= 5:
                cname = chc(divs[0].css("a::text").extract())
                title = chc(divs[1].css("text").extract())
                location = chc(divs[2].css('::text').extract())
                date = chc(divs[3].css('::text').extract())
                dtime = chc(divs[4].css('::text').extract())
                startTime, endTime = CustomUtil.splitTimes(date+" "+dtime)

                # 提取id
                a = gfs(divs[0].css('a').extract())
                m = re.search(self.id_pattern, a)
                if m:
                    sid = m.group(1)
                    url = self.getDetailUrlById(sid)
                    item = self.createItem(sid, title, startTime, endTime, location, None)
                    if self.isNeedToParseDetail(url, item):
                        yield scrapy.Request(url, callback=self.parse_item_detail, meta={'item': item, 'cname': cname})

    def isNeedToParseDetail(self, url, item):
        return url and not DoneSet.isInDoneSet(self, item)

    def parse_item_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        info_dic = {}
        # 采用字典匹配的方法
        trs = response.css('.bd_tab>tr')
        for tr in trs:
            tds = tr.css('tr>td')
            if (len(tds) & 1) == 0:
                i = 0
                key = None
                for td in tds:
                    td = pq(gfs(td.extract()))
                    # print i&1,td.text()
                    if (i&1) == 1:
                        info_dic[key] = td.text().strip()
                    else:
                        key = td.text().strip()
                    i += 1
        cname = info_dic.get(u'单位名称')
        cpro = info_dic.get(u'单位性质')
        chome = info_dic.get(u'应聘网址')
        cemail = info_dic.get(u'简历投递邮箱')
        caddr = info_dic.get(u'单位地址')

        company = CompanyItem(cname, prop=cpro, homePage=chome, email=cemail, addr=caddr)
        infoDetailRaw = response.css('.bd_tab tr:nth-child(4) td').extract()
        item['company'] = company
        item['infoDetailRaw'] = chc(infoDetailRaw)
        return item

    @classmethod
    def getDetailUrlById(cls, tid):
        return cls.detail_url+"&id="+tid


    @staticmethod
    def createItem(sid, title, startTime, endTime, location, issueTime):
        item = SJTUItem()
        item['sid'] = sid
        item['title'] = title
        item['startTime'] = startTime
        item['endTime'] = endTime
        item['location'] = location
        item['issueTime'] = issueTime
        return item