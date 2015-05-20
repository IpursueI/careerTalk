#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

__author__ = 'phk'

import scrapy
from careerTalk import items
import re


class SEUSpider(scrapy.Spider):
    name = "SEU"
    university = u'东南大学'
    infoSource = u'东南大学就业信息网'
    allowed_domains = ["jy.seu.edu.cn"]
    start_urls = [
        "http://jy.seu.edu.cn/detach.portal?.p=Znxjb20ud2lzY29tLnBvcnRhbC5jb250YWluZXIuY29yZS5pbXBsLlBvcnRsZXRFbnRpdHlXaW5kb3d8cGU3ODF8dmlld3xub3JtYWx8YWN0aW9uPXF1ZXJ5QWxsWnBoTWFuYWdlVmlldw__&SFGQ=2&pageIndex=1",
        "http://jy.seu.edu.cn/detach.portal?.p=Znxjb20ud2lzY29tLnBvcnRhbC5jb250YWluZXIuY29yZS5pbXBsLlBvcnRsZXRFbnRpdHlXaW5kb3d8cGU3ODF8dmlld3xub3JtYWx8YWN0aW9uPXF1ZXJ5QWxsWnBoTWFuYWdlVmlldw__&SFGQ=1&pageIndex=1"
    ]
    # 已过期的摘要页面的链接
    abs_page_url = "http://jy.seu.edu.cn/detach.portal?.p=Znxjb20ud2lzY29tLnBvcnRhbC5jb250YWluZXIuY29yZS5pbXBsLlBvcnRsZXRFbnRpdHlXaW5kb3d8cGU3ODF8dmlld3xub3JtYWx8YWN0aW9uPXF1ZXJ5QWxsWnBoTWFuYWdlVmlldw__&SFGQ=2"
    # 具体页面的链接
    detail_url= 'http://jy.seu.edu.cn/detach.portal?.pen=pe781&.pmn=view&action=oneView'
    # 将正则表达式编译成Pattern对象
    link_pattern = re.compile(r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')

    def parse(self, response):
        reqs = self.parse_item_s(response)
        for req in reqs:
            yield  req
        # 解析后续页面的内容
        next_urls = self.parse_next_page(response.body)
        print '**********************'
        for url in next_urls:
            print '**********url:', url, '**********'
            yield scrapy.Request(url, callback=self.parse)

    def parse_item_s(self, response):
        reqs = []
        # 包含内容的table
        selector_table = response.css('.portlet-table tr')
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
        for tr in selector_table:
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
                    reqs.append(scrapy.Request(link, callback=self.parse_detail_page, meta={'item': item}))
                else:
                    reqs.append(scrapy.Request(None, callback=self.parse_detail_page, meta={'item': item}))
        return reqs

    def parse_next_page(self, body):
        """
        获取下一个页面的链接
        :param value: 页面内容
        :return: 解析得到的后续页面链接列表
        """
        # <a href="#" onclick="return turnPage('fpe781','6')" title="点击跳转到第6页">6</a>
        # <div title="当前页">3</div>
        urls = []
        it = re.finditer(r"return turnPage\('.*','(\d*)'\)", body)
        curPage = re.search(r'<div title="当前页">(\d*)</div>',body)
        if curPage and it:
            pageInd = int(curPage.group(1))
            for m in it:
                index = m.group(1)
                # print '*'*10, pageInd, index
                if pageInd < int(index) < 4:
                    url = SEUSpider.abs_page_url+"&pageIndex="+index
                    urls.append(url)
        return urls

    def parse_detail_page(self, response):
        item = response.meta['item']
        ta = response.css('.w-zph-title tr:nth-child(3) td:nth-child(2)::text').extract()
        if len(ta):
            item['targetAcademic'] = ta[0]
        tm = response.css('.w-zph-title tr:nth-child(3) td:nth-child(4)::text').extract()
        print ta,tm
        if len(tm):
            item['targetMajor'] = tm[0]
        yield item
