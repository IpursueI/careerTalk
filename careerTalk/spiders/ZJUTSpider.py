# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
import re
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from careerTalk.items import ZJUTItem
from careerTalk.items import CompanyItem
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent

class ZJUTSpider(scrapy.Spider):
    name = "ZJUT"
    start_urls = ["http://job.zjut.edu.cn/job/IndexMotion!ListJobMore?type=2&page.page=1"]
    
    def __init__(self, *args, **kwargs):
        self.start = 0
        super(ZJUTSpider, self).__init__(*args, **kwargs)
        ZJUTDone = os.path.join(os.path.abspath(os.path.dirname(__file__)),"ZJUTDone")
        self.Done = set()
        f = codecs.open(ZJUTDone,'r','utf-8')
        for line in f:
            self.Done.add(line.strip())
        f.close()

    def parse(self, response):

        responseData = response.xpath("//span[@class='zz']/a")
        itemCount = 0

        for sel in responseData:
            item = ZJUTItem()
            item['university'] = u"浙江工业大学"
            item['title'] = sel.xpath("text()").extract()
            item['infoSource'] = u"浙江工业大学就业指导中心"
            detailUrl = chc(sel.xpath("@href").extract())
            item['sid'] = detailUrl[detailUrl.index('=')+1:detailUrl.index('&')]
            if chc(item['title'])+'_'+chc(item['sid']) in self.Done:
                itemCount += 1
                continue

            url = detailUrl
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
        infoTemp = chc(response.xpath("//div[@id='zph']/h5/text()").extract())
        index = infoTemp.index(' ')
        item['startTime'] = infoTemp[:index]
        item['location'] = infoTemp[index+1:]
        #item['image_urls'] = response.xpath("//div[@class='vContent']//img/@src").extract() 
        item['infoDetailRaw'] = response.xpath("//div[@class='gs']").extract()
        #item['company']  = CompanyItem()
        #item['company']['introduction'] = response.xpath("//div[@class='vContent cl']/div").extract()
        yield item 

    def parse_next_page(self, response):
        if self.start == 0:
            itemCount = int(re.search(r'pager.itemCount = (\d+)',response.body).group(1))
            pageSize = int(re.search(r'pager.size = (\d+)',response.body).group(1))
            if itemCount%pageSize != 0: 
                self.pageCount = itemCount/pageSize+1
            else:
                self.pageCount = itemCount/pageSize
            self.start = 1

        currentPage = int(response.url[response.url.rindex('=')+1:])
        if currentPage+1 <= self.pageCount:
            url = '%s%d' % ('http://job.zjut.edu.cn/job/IndexMotion!ListJobMore?type=2&page.page=', currentPage+1)
            return url 


