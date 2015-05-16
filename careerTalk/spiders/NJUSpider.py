# -*- coding:utf-8 -*-

import scrapy
from careerTalk.items import NJUItem
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent

class NJUSpider(scrapy.spider.Spider):
    name = "NJU"
    start_urls = ["http://job.nju.edu.cn/login/nju/home.jsp?type=zph&pageNow=1"]

    def parse(self, response):
        for sel in response.xpath("//div[@class='article-lists']/ul/li"):
            item = NJUItem()
            item['university'] = u"南京大学"
            item['title'] = chc(sel.xpath("span[1]/a/text()").extract())
            item_t =  chc(sel.xpath("span[2]/text()").extract()).split()
            item['location'] = item_t[0]
            item['startTime'] = item_t[1]+' '+item_t[2]
            item['infoSource'] = u"南京大学就业创业信息网"

            url = response.url[:response.url.rindex('/')+1] + chc(sel.xpath("span[1]/a/@href").extract())
            request = scrapy.Request(url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request

    def parse_detail(self, response):
        item = response.meta['item']
        stmp = chc(response.xpath("//div[@class='article-info']").extract())
        start = stmp.find("</span>")
        start = stmp.find("</span>",start+1)
        end = stmp.find("<span",start)
        item['issueTime'] = stmp[start+7:end].strip()
        #item['infoDetail'] = response.xpath("//table[@class='job_detail']").extract()[0].strip()
        yield item 
