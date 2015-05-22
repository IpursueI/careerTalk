#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

__author__ = 'phk'

import scrapy
from careerTalk import items
import re


class SEUSpider(scrapy.Spider):
    """
    用于抓取东南大学招聘会信息
    遇到问题：get摘要页面的url时，有一定概率会返回详细页面，获取详细页面时，则有可能返回摘要页面，因此需要判断数据是否获取正常，如果数据异常，则进行多次尝试。
    """
    name = "SEU"
    university = u'东南大学'
    infoSource = u'东南大学就业信息网'
    allowed_domains = ["jy.seu.edu.cn"]
    start_urls = [
        # 历史数据
        # "http://jy.seu.edu.cn/detach.portal?.p=Znxjb20ud2lzY29tLnBvcnRhbC5jb250YWluZXIuY29yZS5pbXBsLlBvcnRsZXRFbnRpdHlXaW5kb3d8cGU3ODF8dmlld3xub3JtYWx8YWN0aW9uPXF1ZXJ5QWxsWnBoTWFuYWdlVmlldw__&SFGQ=2&pageIndex=1",

        # 新数据
        "http://jy.seu.edu.cn/detach.portal?.p=Znxjb20ud2lzY29tLnBvcnRhbC5jb250YWluZXIuY29yZS5pbXBsLlBvcnRsZXRFbnRpdHlXaW5kb3d8cGU3ODF8dmlld3xub3JtYWx8YWN0aW9uPXF1ZXJ5QWxsWnBoTWFuYWdlVmlldw__&SFGQ=1&pageIndex=1"
    ]
    # 已过期的摘要页面的链接
    abs_page_url = "http://jy.seu.edu.cn/detach.portal?.p=Znxjb20ud2lzY29tLnBvcnRhbC5jb250YWluZXIuY29yZS5pbXBsLlBvcnRsZXRFbnRpdHlXaW5kb3d8cGU3ODF8dmlld3xub3JtYWx8YWN0aW9uPXF1ZXJ5QWxsWnBoTWFuYWdlVmlldw__"
    # 具体页面的链接
    detail_url= 'http://jy.seu.edu.cn/detach.portal?.pen=pe781&.pmn=view&action=oneView'
    # 将正则表达式编译成Pattern对象
    link_pattern = re.compile(r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
    # 有时获取页面结果是202，可是页面内容却是招聘会详情，于是需要手动重试
    # key值为 abs_{page} 或者 detail_{id} ，value值为尝试的次数
    trySet = {}

    @classmethod
    def getTryCnt(cls, ind, kind='abs_'):
        tid = kind+str(ind)
        return cls.trySet.get(tid, 0)

    @classmethod
    def addTryCnt(cls, ind, kind='abs_'):
        tid = kind+str(ind)
        cls.trySet.setdefault(tid, 0)
        cls.trySet[tid] += 1

    @classmethod
    def canTryAgain(cls, ind, kind='abs_'):
        tid = kind+str(ind)
        return cls.trySet.get(tid, 0) < 3

    def parse(self, response):
        print "\ncurPage:", response.url.split("&")[1:]
        reqs = self.parse_item_s(response)
        # 如果获取的页面是招聘详情页，则不会有任何摘要信息，那么对当前页面进行重新抓取
        if len(reqs) == 0:
            m = re.search(r'pageIndex=(\d+)', response.url)
            if m:
                ind = int(m.group(1))
                if self.canTryAgain(ind):
                    # 附加上一个参数，避免被request的去重机制删除
                    url = response.url + "&try_%d" % self.getTryCnt(ind)
                    self.addTryCnt(ind)
                    yield scrapy.Request(url, callback=self.parse)
        else:
            for req in reqs:
                yield req

        # 解析后续页面的内容
        #
        sfgq = '&SFGQ=1'
        if not re.search(sfgq, response.url):
            sfgq = '&SFGQ=2'
        next_pages = self.parse_next_page(response)
        for index in next_pages:
            url = SEUSpider.abs_page_url+("%s&pageIndex=%d" % (sfgq, index))
            yield scrapy.Request(url, callback=self.parse)
        print 'nextPages:', next_pages
        print

    def parse_item_s(self, response):
        reqs = []
        # 包含内容的table
        selector_table = response.css('.portlet-table tr')
        # 需要解析的数据分布在对应的某一列
        dataSelectorDic = {
            'kind': 'td:nth-child(1)::text',
            'location': 'td:nth-child(2)::text',
            'startTime_date': 'td:nth-child(3)::text',
            'startTime_time': 'td:nth-child(4)::text',
            'sponsor': 'td:nth-child(5) a::text',
            'title': 'td:nth-child(5) a::text'
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
                    item['absLink'] = response.url
                    item['sid'] = item_id[0]
                    reqs.append(scrapy.Request(link, callback=self.parse_detail_page, meta={'item': item}))
                else:
                    reqs.append(scrapy.Request(None, callback=self.parse_detail_page, meta={'item': item}))
        return reqs

    def parse_next_page(self, response):
        """
        获取下一个页面的链接
        :param value: 页面内容
        :return: 解析得到的后续页面编号列表，如果页面内容异常，则加入-1
        """
        # <a href="#" onclick="return turnPage('fpe781','6')" title="点击跳转到第6页">6</a>
        # <div title="当前页">3</div>
        nextPages = []

        it = re.finditer(r"return turnPage\('.*','(\d*)'\)", response.body)
        curPage = re.search(r'<div title="当前页">(\d*)</div>', response.body)
        if curPage and it:
            curPage = int(curPage.group(1))
            inds = []
            for m in it:
                index = int(m.group(1))
                inds.append(index)
                # todo 仅仅只使用下一页进行测试
                if curPage == index-1:
                # if curPage < index:
                    nextPages.append(index)
            print ("curPage:%s relPages:" % curPage), inds
        return nextPages

    def parse_detail_page(self, response):
        item = response.meta['item']
        title = response.css('.w-employee-title')
        # 如果数据错误，则进行重试
        if not title:
            ind = item['sid']
            if self.canTryAgain(ind, kind='detail_'):
                url = response.url + "&try_%d" % self.getTryCnt(ind, kind='detail_')
                self.addTryCnt(ind, kind='detail_')
                yield scrapy.Request(url, callback=self.parse_detail_page, meta={'item': item})

        # 正常解析数据
        ta = response.css('.w-zph-title tr:nth-child(3) td:nth-child(2)::text').extract()
        if len(ta):
            item['targetAcademic'] = ta[0]
        tm = response.css('.w-zph-title tr:nth-child(3) td:nth-child(4)::text').extract()
        # print ta,tm
        if len(tm):
            item['targetMajor'] = tm[0]
        yield item
