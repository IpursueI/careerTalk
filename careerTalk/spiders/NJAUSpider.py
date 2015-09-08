# -*- coding:utf-8 -*-

import scrapy
import os
import codecs
import re
import urllib2
import urllib, httplib
from scrapy.exceptions import CloseSpider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from careerTalk.items import NJAUItem
from careerTalk.items import CompanyItem
from careerTalk.customUtil import CustomUtil
from urllib import urlencode
chc = CustomUtil.convertHtmlContent

class NJAUSpider(scrapy.Spider):
    name = "NJAU"
    start_urls = ["http://xszj.njau.edu.cn/WebSite/Employment/TempRecruitList.aspx?h=1"]
    
    def __init__(self, *args, **kwargs):
        super(NJAUSpider, self).__init__(*args, **kwargs)
        NJAUDone = os.path.join(os.path.abspath(os.path.dirname(__file__)),"NJAUDone")
        self.Done = set()
        f = codecs.open(NJAUDone,'r','utf-8')
        for line in f:
            self.Done.add(line.strip())
        f.close()

    def parse(self, response):
        # responseData = response.xpath("//div[@id='Content']/table//tr/td[2]")
        # itemCount = 0
        f = open('tmpData2.txt','a')
        f.write(response.body)
        f.write('\n')
        f.close()
        # for sel in responseData:
        #     item = NJAUItem()
        #     item['university'] = u"南京农业大学"
        #     item['title'] = sel.xpath("a/text()").extract()
        #     #item['location'] = sel.xpath("li[4]/text()").extract()
        #     item['startTime'] = sel.xpath("font/text()").extract()
        #     item['infoSource'] = u"南京农业大学就业指导与服务中心"
        #     detailUrl = chc(sel.xpath("a/@href").extract())
        #     item['sid'] = detailUrl[detailUrl.index('=')+1:]
        #     if chc(item['title'])+'_'+chc(item['sid']) in self.Done:
        #         itemCount += 1
        #         continue

            # url = response.url[:response.url.rindex('/')+1] + detailUrl
            # request = scrapy.Request(url,callback=self.parse_detail)
            # request.meta['item'] = item
            # yield request


        data = self.parse_next_page(response)
        f = open('tmpData.txt','a')
        f.write(data[0])
        f.write('\n')
        f.close()

        req = urllib2.urlopen(url=data[1],data=data[0])
        f = open('tmpData3.txt','a')
        f.write(req.read())
        f.write('\n')
        f.close()
        yield scrapy.Request(data[1],  method='POST', body=data[0], callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        item['link'] = response.url
        item['company']  = CompanyItem()
        #item['image_urls'] = response.xpath("//div[@class='vContent']//img/@src").extract() 
        #item['infoDetailRaw'] = response.xpath("//div[@class='vContent']").extract()
        #item['company']  = CompanyItem()
        #item['company']['introduction'] = response.xpath("//div[@class='vContent cl']/div").extract()
        yield item

    def parse_next_page(self, response):
        # theaders = {
        #         'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        #         'Accept-Encoding':'gzip, deflate',
        #         'Accept-Language':'zh-CN,zh;q=0.8',
        #         'Cache-Control':'max-age=0',
        #         'Connection':'keep-alive',
        #         'Content-Length':'21052',
        #         'Content-Type':'application/x-www-form-urlencoded',
        #         'Cookie':'ASP.NET_SessionId=d5ymrvgb105bdmow3ho4mepo; safedog-flow-item=E197BF651F0F186F43DE25916AEB35D7; CNZZDATA1000273143=1658095116-1432722239-%7C1433222799',
        #         'Host':'http://xszj.njau.edu.cn',
        #         'Origin':'http://xszj.njau.edu.cn',
        #         'Referer':'http://xszj.njau.edu.cn/WebSite/Employment/TempRecruitList.aspx',
        #         'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36'
        #         }
        eventTarget = 'lbnNextPage'
        eventArgument = ''
        viewState = chc(response.xpath("//input[@name='__VIEWSTATE']/@value").extract())
        viewstateGenerator = chc(response.xpath("//input[@name='__VIEWSTATEGENERATOR']/@value").extract())
        eventValidation = chc(response.xpath("//input[@name='__EVENTVALIDATION']/@value").extract())
        loginName = ''
        loginPass = ''
        loginType = 'S'
        num = ''
        
        tbody = { 
                '__EVENTTARGET':eventTarget,
                '__EVENTARGUMENT':eventArgument,
                '__VIEWSTATE':viewState,
                '__VIEWSTATEGENERATOR':viewstateGenerator,
                '__EVENTVALIDATION':eventValidation,
                'top1$LoginName':loginName,
                'top1$LoginPass':loginPass,
                'top1$LoginType':loginType,
                'Num':num
                }
        
        tbody = urlencode(tbody)
        ind = response.url.rindex('=')
        num = int(response.url[ind+1:])
        url = '%s%d' % (response.url[:ind+1], num+1)
        return tbody,url
        


