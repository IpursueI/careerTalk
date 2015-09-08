# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
import re
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from careerTalk.items import HHUItem
from careerTalk.items import CompanyItem
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent

class HHUSpider(scrapy.Spider):
    name = "HHU"
    start_urls = ["http://job.hhu.edu.cn/s/93/t/342/p/32/i.htm"]
    
    def __init__(self, *args, **kwargs):
        super(HHUSpider, self).__init__(*args, **kwargs)
        HHUDone = os.path.join(os.path.abspath(os.path.dirname(__file__)),"HHUDone")
        self.Done = set()
        f = codecs.open(HHUDone,'r','utf-8')
        for line in f:
            self.Done.add(line.strip())
        f.close()

    def parse(self, response):

        if(response.url == 'http://job.hhu.edu.cn/s/93/t/342/p/32/i.htm'):
            totalItem = int(response.body.strip())
            self.totalPages = totalItem/14
            start = '%s%d%s' % ('http://job.hhu.edu.cn/s/93/t/342/p/32/i/', totalItem/14, '/list.htm')
            yield scrapy.Request(start,callback=self.parse)
        else:
            responseData = response.xpath("//table[@class='columnStyle']//tr")
            itemCount = 0

            for sel in responseData:
                item = HHUItem()
                item['university'] = u"河海大学"
                item['title'] = sel.xpath("td[1]//font/text()").extract()
                item['issueTime'] = sel.xpath("td[2]/text()").extract()
                item['infoSource'] = u"河海大学学生就业信息网"
                detailUrl = chc(sel.xpath("td[1]/a/@href").extract())
                sIndex = detailUrl.rindex('/')+5
                eIndex = detailUrl.rindex('.')
                item['sid'] = detailUrl[sIndex : eIndex]
                if chc(item['title'])+'_'+chc(item['sid']) in self.Done:
                    itemCount += 1
                    continue

                url = response.url[:response.url.index('cn')+2] + detailUrl
                request = scrapy.Request(url,callback=self.parse_detail)
                request.meta['item'] = item
                yield request

            nextUrl = self.parse_next_page(response)
            if nextUrl:
                yield scrapy.Request(nextUrl, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        item['infoDetailRaw'] = response.xpath("//div[@class='wznr']").extract()
        item['company']  = CompanyItem()
        #item['image_urls'] = response.xpath("//div[@class='vContent']//img/@src").extract() 
        #item['infoDetailRaw'] = response.xpath("//div[@class='vContent']").extract()
        #item['location'] = response.xpath("//div[@class='wznr']/span/div[4]/span/text()").extract()
        #date = chc(response.xpath("//div[@class='wznr']/span/div[5]/span/text()").extract())
        #time = chc(response.xpath("//div[@class='wznr']/span/div[6]/span/text()").extract())
        #item['startTime'] = date + ' ' + time
        #detail1 =u'针对学历：\n' +  chc(response.xpath("//div[@class='wznr']/span/div[7]/span/text()").extract()) + '\n'
        #detail2 =u'针对专业：\n' +  chc(response.xpath("//div[@class='wznr']/span/div[8]/span/text()").extract()) + '\n'
        #detail3 =u'相关链接：\n' +  chc(response.xpath("//div[@class='wznr']/span/div[13]/span/text()").extract()) + '\n'
        #detail4 =u'备注：\n' +  chc(response.xpath("//div[@class='wznr']/span/div[14]/span/text()").extract()) + '\n'
        #item['infoDetailText'] = detail1 + detail2 + detail3 + detail4 
        #item['company']  = CompanyItem()
        #item['company']['introduction'] = response.xpath("//div[@class='vContent cl']/div").extract()
        yield item 

    def parse_next_page(self, response):
        self.totalPages -= 1
        if self.totalPages >= 1:
            url = '%s%d%s' % ('http://job.hhu.edu.cn/s/93/t/342/p/32/i/', self.totalPages,'/list.htm' )
            return url 


