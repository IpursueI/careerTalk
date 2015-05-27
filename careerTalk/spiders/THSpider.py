#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

__author__ = 'phk'


import datetime
import time
import json
import re

from careerTalk.items import THItem,CompanyItem
import scrapy
from careerTalk.customUtil import CustomUtil, DoneSet

chc = CustomUtil.convertHtmlContent
gfs = CustomUtil.getFirstStr


class THSpider(scrapy.Spider):
    name = "TH"
    allowed_domains = ["career.cic.tsinghua.edu.cn"]

    # 设置下载延时
    download_delay = 0.25

    # 可以通过该url获取到宣讲会的摘要数据,需要加入参数 【日期】
    # http://career.cic.tsinghua.edu.cn/xsglxt/b/jyxt/anony/queryTodayHdList?callback=&rq=2015-05-05
    abs_url = "http://career.cic.tsinghua.edu.cn/xsglxt/b/jyxt/anony/queryTodayHdList?callback=&rq="
    start_urls = []
    today = datetime.datetime.today()
    # 获取前一个月与后两个月的日期，并将其加入start_url中
    for i in range(-30, 60):
        delta = datetime.timedelta(days=i)
        curT = today-delta
        strT = curT.date().strftime("%Y-%m-%d")
        start_urls.append(abs_url+strT)

    # 具体页面的链接
    # http://career.cic.tsinghua.edu.cn/xsglxt/f/jyxt/anony/gotoZpxxList?id=1506020626
    detail_url = "http://career.cic.tsinghua.edu.cn/xsglxt/f/jyxt/anony/gotoZpxxList?id="

    def parse(self, response):
        return self.parse_items(response)
        # 并不需要解析下一个页面，start_urls包含了所有要解析的数据

    def parse_items(self, response):
        # 返回的是json数据
        # ([{"rq":"20150505","zphid":"1506020626","sfzb":"否","jssj":"21:00","kssj":"19:00","cdmcqc":"二教会议室","fblx":"专场","bt":"美的集团家用空调事业部-博士座谈会"}])
        body = response.body
        datas = json.loads(body[1:-1])
        print datas
        for data in datas:
            sid = data['zphid']
            startTime = data['rq']+data['kssj']
            endTime = data['rq']+data['jssj']
            location = data['cdmcqc']
            title = data['bt']

            t_pattern = r"\d{4}\d{2}\d{2}\d{2}:\d{2}"
            if re.match(t_pattern,startTime):
                startTime = time.strptime(startTime, "%Y%m%d%H:%M")
                startTime = time.strftime(CustomUtil.time_format, startTime)
            else:
                startTime = time.strptime(startTime, "%Y%m%d")
                startTime = time.strftime(CustomUtil.time_format, startTime)
            if re.match(t_pattern,endTime):
                endTime = time.strptime(endTime, "%Y%m%d%H:%M")
                endTime = time.strftime(CustomUtil.time_format, endTime)
            else:
                endTime = time.strptime(endTime, "%Y%m%d")
                endTime = time.strftime(CustomUtil.time_format, endTime)

            item = self.createItem(sid, title, startTime, endTime, location)

            url = self.detail_url+sid

            if self.isNeedToParseDetail(url, item):
                yield scrapy.Request(url, callback=self.parse_item_detail, meta={'item': item})

    def isNeedToParseDetail(self, url, item):
        return url and not DoneSet.isInDoneSet(self, item)

    def parse_item_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        infoDetailRaw = None

        item['infoDetailRaw'] = infoDetailRaw

        cname = chc(response.css('h1.title::text').extract())
        cintro = response.css('.company-introduction').extract()
        cintro = CustomUtil.h2t(gfs(cintro))

        infos = response.css('#comTab tr')
        info_dic = {}
        for tr in infos:
            th = chc(tr.css('th::text').extract())
            td = chc(tr.css('td::text').extract())
            if th and td:
                info_dic[gfs(th).strip()] = gfs(td).strip()
        cpro = info_dic.get(u'公司性质：')
        cscale = info_dic.get(u'公司规模：')
        cind = info_dic.get(u'公司行业：')

        company = CompanyItem(cname,
                              intro=cintro,
                              prop=cpro,
                              scale=cscale,
                              industry=cind)
        item['company'] = company
        return item

    @staticmethod
    def createItem(sid, title, startTime, endTime, location):
        item = THItem()
        item['sid'] = sid
        item['title'] = title
        item['startTime'] = startTime
        item['endTime'] = endTime
        item['location'] = location
        return item