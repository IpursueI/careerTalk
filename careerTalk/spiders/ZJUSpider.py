# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
import re
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from careerTalk.items import ZJUItem
from careerTalk.items import CompanyItem
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent
getDone = CustomUtil.getDoneSet

class ZJUSpider(scrapy.Spider):
    name = "ZJU"
    start_urls = ["http://www.career.zju.edu.cn/ejob/zczphxxmorelogin.do?pages.currentPage=1"]
    
    def __init__(self, *args, **kwargs):
        super(ZJUSpider, self).__init__(*args, **kwargs)
        self.totalPages = 0
        self.Done = getDone(self.name)

    def parse(self, response):

        responseData = response.xpath("//tr[@class='con']")
        itemCount = 0

        for sel in responseData:
            item = ZJUItem()
            item['university'] = u"浙江大学"
            item['title'] = sel.xpath("td[1]/a/text()").extract()
            item['location'] = sel.xpath("td[2]/text()").extract()
            item['startTime'] = sel.xpath("td[3]/text()").extract()
            item['infoSource'] = u"浙江大学就业指导与服务中心"
            detailUrl = chc(sel.xpath("td[1]/a/@href").extract())
            item['sid'] = detailUrl[detailUrl.rindex('=')+1:]
            if chc(item['title'])+'_'+chc(item['sid']) in self.Done:
                itemCount += 1
                continue

            url = response.url[:response.url.rindex('/')+1] + detailUrl
            request = scrapy.Request(url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request

        nextUrl = self.parse_next_page(response)
        if nextUrl:
            yield scrapy.Request(nextUrl, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        #item['image_urls'] = response.xpath("//div[@class='vContent']//img/@src").extract() 
        info = response.xpath("//form[@name='zpxxglActionForm']/table/tr").extract()
        item['infoDetailRaw'] = info[-1]
        item['company']  = CompanyItem()
        item['company']['introduction'] = response.xpath("//div[@id='cent']/div[2]").extract()
        yield item 

    def parse_next_page(self, response):
        if self.totalPages == 0:
            self.totalPages = int(re.search(r'name="pages.maxPage" value="(\d+)"',response.body).group(1))
        currentPage = int(response.url[response.url.rindex('=')+1:])
        if currentPage+1 <= self.totalPages:
            url = '%s%d' % ('http://www.career.zju.edu.cn/ejob/zczphxxmorelogin.do?pages.currentPage=',currentPage+1)
            return url 


