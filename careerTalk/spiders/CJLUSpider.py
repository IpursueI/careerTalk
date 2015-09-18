# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
import re
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from careerTalk.items import CJLUItem
from careerTalk.items import CompanyItem
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent
getDone = CustomUtil.getDoneSet

class CJLUSpider(scrapy.Spider):
    name = "CJLU"
    start_urls = ["http://jyb.cjlu.edu.cn/newsList.asp?page=1&firstCategoryId=86&secondCategoryId=87&flag="]
    
    def __init__(self, *args, **kwargs):
        super(CJLUSpider, self).__init__(*args, **kwargs)
        self.Done = getDone(self.name)

    def parse(self, response):

        responseData = response.xpath("//div[@class='newsListBody']/a")
        itemCount = 0

        for sel in responseData:
            item = CJLUItem()
            item['university'] = u"中国计量学院"
            item['title'] = sel.xpath("text()").extract()
            item['infoSource'] = u"中国计量学院就业指导中心"
            detailUrl = chc(sel.xpath("@href").extract())
            item['sid'] = detailUrl[detailUrl.rindex('=')+1:]
            if chc(item['title'])+'_'+chc(item['sid']) in self.Done:
                itemCount += 1
                continue

            url = response.url[:response.url.rindex('cn')+3] + detailUrl
            request = scrapy.Request(url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request


        nextUrl = self.parse_next_page(response)
        if nextUrl:
            yield scrapy.Request(nextUrl, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        item['infoDetailRaw'] = response.xpath("//div[@class='content']/table//tr[4]/td").extract()
        item['company']  = CompanyItem()
        yield item 

    def parse_next_page(self, response):
        m =  re.findall(ur'<A href="\?page=(\d+)',response.body)
        if m:
            url = 'http://jyb.cjlu.edu.cn/newsList.asp?Page='+m[-1]+'&firstCategoryId=86&secondCategoryId=87&flag='
            return url
