# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
import re
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from careerTalk.items import ZJGSUItem
from careerTalk.items import CompanyItem
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent
getDone = CustomUtil.getDoneSet

class ZJGSUSpider(scrapy.Spider):
    name = "ZJGSU"
    start_urls = ["http://jyw.zjgsu.edu.cn/Articlelist.asp?nid=24&me_page=1"]
    
    def __init__(self, *args, **kwargs):
        super(ZJGSUSpider, self).__init__(*args, **kwargs)
        self.Done = getDone("ZJGSUDone")

    def parse(self, response):

        responseData = response.xpath("//body/table/tr/td/table/tr/td/table/tr/td/table[@cellpadding='4']/tr")
        itemCount = 0

        for sel in responseData:
            item = ZJGSUItem()
            item['university'] = u"浙江工商大学"
            tmpData = sel.xpath("td[2]/a/text()").extract()[0]
            item['title'] = tmpData.split()[0]
            #self.get_date_location(tmpData, item)
            item['infoSource'] = u"浙江工商大学毕业生就业信息网"
            item['issueTime'] = sel.xpath("td[3]/text()").extract()[0]
            detailUrl = chc(sel.xpath("td[2]/a/@href").extract())
            item['sid'] = detailUrl[detailUrl.index('=')+1:]
            if chc(item['title'])+'_'+item['sid'] in self.Done:
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
        company = CompanyItem()
        company['name'] = response.xpath("/html/body/table[2]//tr/td[3]/table//tr[2]/td/table//tr[3]/td//table//tr[2]/td[1]/p").extract()
        item['company'] = company
        time1 = chc(response.xpath("/html/body/table[2]//tr/td[3]/table//tr[2]/td/table//tr[3]/td//table//tr[2]/td[2]/p").extract())
        time2 = chc(response.xpath("/html/body/table[2]//tr/td[3]/table//tr[2]/td/table//tr[3]/td//table//tr[2]/td[3]/p").extract())
        item['startTime'] = time1 + time2
        item['location'] = response.xpath("/html/body/table[2]//tr/td[3]/table//tr[2]/td/table//tr[3]/td//table//tr[2]/td[4]/p").extract()
        item['infoDetailRaw'] = response.xpath("/html/body/table[2]//tr/td[3]/table//tr[2]/td/table//tr[3]/td").extract()
        yield item 

    def parse_next_page(self, response):
        m1 = re.search(ur"<a href='javascript:viewPage\((\d+)\)' language='javascript'>\xcf\xc2\xd2\xb3",response.body)
        m2 = re.search(r"<a href=\'javascript:viewPage\((\d+)\)\' language =\'javascript\'>\xcf\xc2\xd2\xb3",response.body)
        if m1:
            url = 'http://jyw.zjgsu.edu.cn/Articlelist.asp?nid=24&me_page='+m1.group(1)
            return url 
        if m2:
            url = 'http://jyw.zjgsu.edu.cn/Articlelist.asp?nid=24&me_page='+m2.group(1)
            return url 

    #def get_date_location(self, data, item):
    #    item['title'] = data.split()[0]
    #    item['location'] = ' '.join(re.findall(ur'[A-Za-z]\d+', data))
    #    item['startTime'] = ' '.join(re.findall(ur'\d+\u6708\d+\u65e5.*?\d+\uff1a\d+\u2014\d+\uff1a\d+|\d+\.\d+|\d+\u6708\d+\u65e5', data))


