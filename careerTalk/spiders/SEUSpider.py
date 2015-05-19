#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

__author__ = 'phk'

import scrapy
from careerTalk import items
import re


class SEUSpider(scrapy.spider.Spider):
    name = "SEU"
    university = u'东南大学'
    infoSource = u'东南大学就业信息网'
    allowed_domains = ["jy.seu.edu.cn"]
    start_urls = [
        "http://jy.seu.edu.cn/detach.portal?.p=Znxjb20ud2lzY29tLnBvcnRhbC5jb250YWluZXIuY29yZS5pbXBsLlBvcnRsZXRFbnRpdHlXaW5kb3d8cGU3ODF8dmlld3xub3JtYWx8YWN0aW9uPXF1ZXJ5QWxsWnBoTWFuYWdlVmlldw__&pageIndex=1"
    ]
    # 具体页面的链接
    detail_url= 'http://jy.seu.edu.cn/detach.portal?.pen=pe781&.pmn=view&action=oneView'
    # 将正则表达式编译成Pattern对象
    link_pattern = re.compile(r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')

    def parse(self, response):
        # 包含内容的table
        table = response.css('.portlet-table tr')
        # 需要解析的数据分布在对应的某一列
        dataSelectorDic = {
            'kind': 'td:nth-child(1)::text',
            'location': 'td:nth-child(2)::text',
            'startDate': 'td:nth-child(3)::text',
            'startTime': 'td:nth-child(4)::text',
            'sponsor': 'td:nth-child(5) a::text'
        }
        linkCss = 'td:nth-child(6) a'
        # 解析每一行
        for tr in table:
            item = items.SEUItem()
            item['university'] = SEUSpider.university
            item['infoSource'] = SEUSpider.infoSource
            for key in dataSelectorDic.keys():
                val = tr.css(dataSelectorDic[key]).extract()
                # 表格头部并没有对应数据
                if len(val) != 0:
                    item[key] = val[0]
            if item.get('kind') and item['kind'].__contains__(u'宣讲会'):
                # 获取具体连接
                item_id = tr.css(linkCss).re(SEUSpider.link_pattern)
                # 获取详细信息
                if len(item_id) != 0:
                    link = SEUSpider.detail_url+'&zphbh='+item_id[0]
                    item['link'] = link
                    item['sid'] = item_id[0]
                    yield scrapy.Request(link, callback=self.parse_detail_page, meta={'item': item})
                else:
                    yield scrapy.Request(None, callback=self.parse_detail_page, meta={'item': item})

    def parse_detail_page(self, response):
        item = response.meta['item']
        ta = response.css('.w-zph-title tr:nth-child(3) td:nth-child(2)::text').extract()
        if len(ta):
            item['targetAcademic'] = ta[0]
        tm = response.css('.w-zph-title tr:nth-child(3) td:nth-child(4)::text').extract()
        print ta,tm
        if len(tm):
            item['targetMajor'] = tm[0]
        # item['detailInfo'] = None
        # return item
        yield item
        # yield scrapy.Request("http://jy.seu.edu.cn", callback=self.test)

    def test(self, response):
        item = items.BaseItem()
        item['title'] = response.css('title::text').extract()[0]
        yield item