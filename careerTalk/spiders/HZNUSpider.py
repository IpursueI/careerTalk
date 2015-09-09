# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
import re
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from careerTalk.items import HZNUItem
from careerTalk.items import CompanyItem
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent
getDone = CustomUtil.getDoneSet

class HZNUSpider(scrapy.Spider):
    name = "HZNU"
    start_urls = ["http://job.hznu.edu.cn/view/ind_applies.do?pageNo=1&rId="]
    
    def __init__(self, *args, **kwargs):
        super(HZNUSpider, self).__init__(*args, **kwargs)
        self.Done = getDone("HZNUDone")

    def parse(self, response):

        responseData = response.xpath("//div[@class='post']//tbody/tr")
        itemCount = 0

        for sel in responseData:
            item = HZNUItem()
            item['university'] = u"杭州师范大学"
            item['title'] = sel.xpath("td[1]/a[@target='_blank']/font/text()").extract()
            item['location'] = sel.xpath("td[2]/text()").extract()
            item['startTime'] = sel.xpath("td[3]/text()").extract()
            item['infoSource'] = u"杭州师范大学就业创业网"
            detailUrl = chc(sel.xpath("td[1]/a[@target='_blank']/@href").extract())
            item['sid'] = detailUrl[detailUrl.rindex('=')+1:]
            if chc(item['title'],1)+'_'+chc(item['sid']) in self.Done:
                itemCount += 1
                continue

            url = detailUrl
            request = scrapy.Request(url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request

        nextUrl = self.parse_next_page(response)
        if nextUrl:
            yield scrapy.Request(nextUrl, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        item['infoDetailRaw'] = response.xpath("//div[@class='posinfo'][1]").extract()
        item['company']  = CompanyItem()
        item['company']['introduction'] = response.xpath("//div[@class='posinfo'][2]").extract()
        yield item 

    def parse_next_page(self, response):
        m = re.search(r"pageNo=(\d+)&rId=' class='nextPage", response.body)
        if m:
            url = 'http://job.hznu.edu.cn/view/ind_applies.do?pageNo='+m.group(1)+'&rId='
            return url 


