import scrapy

class NJUSpider(scrapy.spider.Spider):
    name = "NJU"
    start_urls = [http://job.nju.edu.cn/login/nju/home.jsp?type=zph&pageNow=1]

    def parse(self, response):
        
