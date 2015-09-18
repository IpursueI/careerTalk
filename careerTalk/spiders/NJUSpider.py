# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
import re
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from careerTalk.items import NJUItem
<<<<<<< HEAD
from careerTalk.items import CompanyItem
from careerTalk.customUtil import CustomUtil
=======
from careerTalk.customUtil import CustomUtil, DoneSet
>>>>>>> dev-phk
chc = CustomUtil.convertHtmlContent
getDone = CustomUtil.getDoneSet


class NJUSpider(scrapy.Spider):
    name = "NJU"
<<<<<<< HEAD
    start_urls = ["http://job.nju.edu.cn/login/nju/home.jsp?type=zph&pageNow=1"]
    
    def __init__(self, *args, **kwargs):
        super(NJUSpider, self).__init__(*args, **kwargs)
        self.Done = getDone("NJUDone")
=======
    start_urls = ["http://job.nju.edu.cn/login/nju/home.jsp?type=zph&pageNow=1",
                  "http://job.nju.edu.cn:9081/login/nju/home.jsp?type=zph&pageNow=1"]
>>>>>>> dev-phk

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
<<<<<<< HEAD
            item['infoSource'] = u"南京大学就业创业信息网"
            detailUrl = chc(sel.xpath("span[1]/a/@href").extract())
            item['sid'] =  detailUrl[detailUrl.index('=')+1:detailUrl.index('type')-1]
            if chc(item['title'])+'_'+chc(item['sid']) in self.Done:
                continue

            url = response.url[:response.url.rindex('/')+1] + detailUrl
            request = scrapy.Request(url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request
=======

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
>>>>>>> dev-phk

    def parse_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        item['issueTime'] = response.xpath("//div[@class='article-info']").re(r'</span>*(.*)')
<<<<<<< HEAD
        item['company'] = CompanyItem()
        item['company']['name'] = item['issueTime'][0]
        item['infoDetailRaw'] = response.xpath("//table[@class='job_detail']").extract()
=======
        item['issueTime'] = chc(item['issueTime'], 1)
        item['infoDetailRaw'] = chc(response.xpath("//table[@class='job_detail']").extract())
>>>>>>> dev-phk
        yield item 
