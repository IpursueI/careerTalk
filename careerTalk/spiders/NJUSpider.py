# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from careerTalk.items import NJUItem
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent

class NJUSpider(scrapy.Spider):
    name = "NJU"
    start_urls = ["http://job.nju.edu.cn/login/nju/home.jsp?type=zph&pageNow=1"]
    
    rules = (
            Rule(LinkExtractor(allow=(r'/home.jsp?type=zph&pageNow=\d+')), callback='parse'),
            )

    def __init__(self, *args, **kwargs):
        super(NJUSpider, self).__init__(*args, **kwargs)
        NJUDone = os.path.join(os.path.abspath(os.path.dirname(__file__)),"NJUDone")
        self.Done = set()
        f = codecs.open(NJUDone,'r','utf-8')
        for line in f:
            self.Done.add(line.strip())
        f.close()

    def parse(self, response):

        for sel in response.xpath("//div[@class='article-lists']/ul/li"):
            item = NJUItem()
            item['university'] = u"南京大学"
            item['title'] = sel.xpath("span[1]/a/text()").extract()
            item_t =  chc(sel.xpath("span[2]/text()").extract()).split()
            item['location'] = item_t[0]
            item['startTime'] = item_t[1]+' '+item_t[2]
            item['infoSource'] = u"南京大学就业创业信息网"
            
            if chc(item['title']) in self.Done:
                continue

            url = response.url[:response.url.rindex('/')+1] + chc(sel.xpath("span[1]/a/@href").extract())
            request = scrapy.Request(url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        item['issueTime'] = response.xpath("//div[@class='article-info']").re(r'</span>*(.*)')
        item['infoDetail'] = response.xpath("//table[@class='job_detail']").extract()
        yield item 
