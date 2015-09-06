# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
import re
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from careerTalk.items import NJUItem
from careerTalk.customUtil import CustomUtil, DoneSet
chc = CustomUtil.convertHtmlContent


class NJUSpider(scrapy.Spider):
    name = "NJU"
    start_urls = ["http://job.nju.edu.cn/login/nju/home.jsp?type=zph&pageNow=1",
                  "http://job.nju.edu.cn:9081/login/nju/home.jsp?type=zph&pageNow=1"]

    id_pattern = re.compile(r'[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
    page_pattern = re.compile(r'home.jsp\?type=zph&pageNow=\d+');

    def isNeedToParseDetail(self, url, item):
        return url and not DoneSet.isInDoneSet(self, item)

    def parse(self, response):
        # 解析不同的item
        for sel in response.xpath("//div[@class='article-lists']/ul/li"):
            item = NJUItem()
            item['title'] = chc(sel.xpath("span[1]/a/text()").extract())
            item_t = chc(sel.xpath("span[2]/text()").extract()).split()
            item['location'] = item_t[0]
            item['startTime'] = item_t[1]+' '+item_t[2]

            url = response.url[:response.url.rindex('/')+1] + chc(sel.xpath("span[1]/a/@href").extract())
            m = re.search(self.id_pattern, url)
            if m:
                sid = m.group()
                item['sid'] = sid
            if self.isNeedToParseDetail(url, item):
                request = scrapy.Request(url, callback=self.parse_detail)
                request.meta['item'] = item
                yield request
        # 获取下一页
        for link in response.xpath("//div[@class='artilce-nav']/a/@href"):
            # self.log(link.extract)
            url = response.url[:response.url.rindex('/')+1] + link.extract()
            m = re.search(self.page_pattern, url)
            if m:
                yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        item['issueTime'] = response.xpath("//div[@class='article-info']").re(r'</span>*(.*)')
        item['issueTime'] = chc(item['issueTime'], 1)
        item['infoDetailRaw'] = chc(response.xpath("//table[@class='job_detail']").extract())
        yield item 
