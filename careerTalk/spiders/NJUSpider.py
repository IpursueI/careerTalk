import scrapy
from careerTalk.items import NJUItem

class NJUSpider(scrapy.spider.Spider):
    name = "NJU"
    start_urls = ["http://job.nju.edu.cn/login/nju/home.jsp?type=zph&pageNow=1"]

    def parse(self, response):
        item = NJUItem()
        item['university'] = response.xpath("//div[@class='article-lists']/ul/li[1]/span[1]/a/text()").extract()

    def parse_page2(self, response):
        pass


