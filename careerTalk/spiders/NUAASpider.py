# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
import re
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from careerTalk.items import NUAAItem
from careerTalk.items import CompanyItem
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent
getDone = CustomUtil.getDoneSet

class NUAASpider(scrapy.Spider):
    name = "NUAA"
    start_urls = ["http://job.nuaa.edu.cn/teachin/index?domain=nuaa&page=1"]
    
    def __init__(self, *args, **kwargs):
        super(NUAASpider, self).__init__(*args, **kwargs)
        self.Done = getDone(self.name)

    def parse(self, response):

        responseData = response.xpath("//ul[@class='infoList teachinList']")
        itemCount = 0

        for sel in responseData:
            item = NUAAItem()
            item['university'] = u"南京航空航天大学"
            item['title'] = sel.xpath("li[1]/a/text()").extract()
            item['location'] = sel.xpath("li[4]/text()").extract()
            item['startTime'] = sel.xpath("li[5]/text()").extract()
            item['infoSource'] = u"南京航空航天大学就业网"
            detailUrl = chc(sel.xpath("li[1]/a/@href").extract())
            item['sid'] = detailUrl[detailUrl.rindex('/')+1:]
            if chc(item['title'])+'_'+chc(item['sid']) in self.Done:
                itemCount += 1
                continue

            url = response.url[:response.url.rindex('/')-8] + detailUrl
            request = scrapy.Request(url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request

        #if itemCount == len(responseData):
        #    raise CloseSpider('already done')

        nextUrl = self.parse_next_page(response)
        if nextUrl:
            yield scrapy.Request(nextUrl, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        item['image_urls'] = response.xpath("//div[@class='vContent']//img/@src").extract() 
        item['infoDetailRaw'] = response.xpath("//div[@class='vContent']").extract()
        item['company']  = CompanyItem()
        item['company']['introduction'] = response.xpath("//div[@class='vContent cl']/div").extract()
        yield item 

    def parse_next_page(self, response):
        m = re.search('<li class="next"><a href="/teachin/index\?domain=nuaa&amp;page=(\d+)',response.body)
        if m:
            url = 'http://job.nuaa.edu.cn/teachin/index?domain=nuaa&page='+m.group(1)
            return url 


