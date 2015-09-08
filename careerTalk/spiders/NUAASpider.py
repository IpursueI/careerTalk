# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
import re
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from careerTalk.items import NUAAItem
from careerTalk.items import CompanyItem
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent

class NUAASpider(scrapy.Spider):
    name = "NUAA"
    start_urls = ["http://job.nuaa.edu.cn/Zph_Index.asp"]
    
    def __init__(self, *args, **kwargs):
        super(NUAASpider, self).__init__(*args, **kwargs)
        NUAADone = os.path.join(os.path.abspath(os.path.dirname(__file__)),"NUAADone")
        self.Done = set()
        f = codecs.open(NUAADone,'r','utf-8')
        for line in f:
            self.Done.add(line.strip())
        f.close()

    def parse(self, response):
        body = response.body.decode('gbk')
        responseData = Selector(text=body).xpath("//table[@class='ntblbk']/tr")[1:]
        itemCount = 0

        for sel in responseData:
            item = NUAAItem()
            item['university'] = u"南京航空航天大学"
            item['title'] = sel.xpath("td/a/text()").extract()
            item['startTime'] = sel.xpath("td[2]/text()").extract()
            item['infoSource'] = u"南京航空航天大学就业指导服务中心"
            detailUrl = chc(sel.xpath("td/a/@onclick").extract())
            reResult = re.search(r"zptype\('3', '(\d+)'\)",detailUrl)
            if reResult is None:
                continue
            else:
                item['sid'] = reResult.group(1)
            if chc(item['title'])+'_'+chc(item['sid']) in self.Done:
                itemCount += 1
                continue

            url = response.url[:response.url.rindex('/')+1] + 'News_View.asp?NewsId=' + item['sid']
            request = scrapy.Request(url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request


    def parse_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        item['issueTime'] = response.xpath("//table[@class='newslisttdbk']/tr[2]/td/text()").extract()[0].split()[0][5:]
        item['infoDetailRaw'] = response.xpath("//table[@class='newslisttdbk']").extract()
        item['company']  = CompanyItem()
        yield item 

