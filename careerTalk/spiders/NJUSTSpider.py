# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
import re
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from careerTalk.items import NJUSTItem
from careerTalk.items import CompanyItem
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent

class NJUSpider(scrapy.Spider):
    name = "NJUST"
    start_urls = ["http://jy.njust.edu.cn/teachin/index?domain=njust&page=1"]
    
    def __init__(self, *args, **kwargs):
        super(NJUSpider, self).__init__(*args, **kwargs)
        NJUSTDone = os.path.join(os.path.abspath(os.path.dirname(__file__)),"NJUSTDone")
        self.Done = set()
        f = codecs.open(NJUSTDone,'r','utf-8')
        for line in f:
            self.Done.add(line.strip())
        f.close()

    def parse(self, response):

        responseData = response.xpath("//ul[@class='infoList teachinList']")
        itemCount = 0

        for sel in responseData:
            item = NJUSTItem()
            item['university'] = u"南京理工大学"
            item['title'] = sel.xpath("li[1]/a/text()").extract()
            item['location'] = sel.xpath("li[4]/text()").extract()
            item['startTime'] = sel.xpath("li[5]/text()").extract()
            item['infoSource'] = u"南京理工大学就业网"
            if chc(item['title'])+' '+chc(item['startTime']) in self.Done:
                itemCount += 1
                continue

            url = response.url[:response.url.rindex('/')-8] + chc(sel.xpath("li[1]/a/@href").extract())
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
        item['image_urls'] = response.xpath("//div[@class='vContent']//img/@src").extract() 
        item['infoDetailRaw'] = response.xpath("//div[@class='vContent']").extract()
        item['company']  = CompanyItem()
        item['company']['introduction'] = response.xpath("//div[@class='vContent cl']/div").extract()
        yield item 

    def parse_next_page(self, response):
        m = re.search('<li class="next"><a href="/teachin/index\?domain=njust&amp;page=(\d+)',response.body)
        if m:
            url = 'http://jy.njust.edu.cn/teachin/index?domain=njust&page='+m.group(1)
            return url 


