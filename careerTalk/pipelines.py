# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import html2text
import json
import codecs
import os
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent


class ItemPipeline(object):
    def process_item(self, item, spider):
        h2t = html2text.HTML2Text()
        h2t.ignore_links = True
        h2t.ignore_images = True

        if spider.name == "NJU":
            item['university'] = chc(item['university'])
            item['title'] = chc(item['title'])
            item['issueTime'] = chc(item['issueTime'],1)
            item['location'] = chc(item['location'])
            item['startTime'] = chc(item['startTime'])
            item['infoSource'] = chc(item['infoSource'])
            item['company']['name'] = chc(item['company']['name'])
            item['company'] = dict(item['company']) 
            item['infoDetailRaw'] = chc(item['infoDetailRaw'])
            item['infoDetailText'] = h2t.handle(item['infoDetailRaw'])
            item['infoDetailRaw'] = ""     #原始数据太多，测试时清空 
            return item

        if spider.name == "NJUST":
            item['university'] = chc(item['university'])
            item['title'] = chc(item['title'])
            item['location'] = chc(item['location'])
            item['startTime'] = chc(item['startTime'])
            item['infoSource'] = chc(item['infoSource'])
            item['infoDetailRaw'] = chc(item['infoDetailRaw'])
            item['infoDetailText'] = h2t.handle(item['infoDetailRaw'])
            item['infoDetailRaw'] = ""     #原始数据太多，测试时清空 
            item['company']['introduction'] = h2t.handle(chc(item['company']['introduction']))
            item['company'] = dict(item['company']) 

            return item

        if spider.name == "NJNU":
            item['university'] = chc(item['university'])
            item['title'] = chc(item['title'])
            item['location'] = chc(item['location'])
            item['startTime'] = chc(item['startTime'])
            item['infoSource'] = chc(item['infoSource'])
            item['infoDetailRaw'] = chc(item['infoDetailRaw'])
            item['infoDetailText'] = h2t.handle(item['infoDetailRaw'])
            item['infoDetailRaw'] = ""     #原始数据太多，测试时清空 
            item['company']['introduction'] = h2t.handle(chc(item['company']['introduction']))
            item['company'] = dict(item['company']) 

            return item

        if spider.name == "ZJGSU":
            item['company']['name'] = h2t.handle(chc(item['company']['name'])).replace('*','').strip()
            item['company'] = dict(item['company']) 
            item['startTime'] = h2t.handle(item['startTime']).replace('*','').strip()
            item['location'] = h2t.handle(chc(item['location'])).replace('*','').strip()
            item['infoDetailRaw'] = chc(item['infoDetailRaw'])
            item['infoDetailText'] = h2t.handle(item['infoDetailRaw'])
            item['infoDetailRaw'] = ""     #原始数据太多，测试时清空 
            return item
            
        if spider.name == "NUAA":
            item['title'] = chc(item['title'])
            item['startTime'] = chc(item['startTime'])
            item['infoDetailRaw'] = chc(item['infoDetailRaw'])
            item['infoDetailText'] = h2t.handle(item['infoDetailRaw'])
            item['infoDetailRaw'] = ""     #原始数据太多，测试时清空 

            return item

        if spider.name == "HHU":
            item['title'] = chc(item['title'])
            item['issueTime'] = chc(item['issueTime'])
            item['infoDetailRaw'] = chc(item['infoDetailRaw'])
            item['infoDetailText'] = h2t.handle(item['infoDetailRaw'])
            item['infoDetailRaw'] = ""     #原始数据太多，测试时清空 

            return item

        if spider.name == "CAA":
            item['university'] = chc(item['university'])
            item['title'] = chc(item['title'])
            item['location'] = chc(item['location'])
            item['startTime'] = chc(item['startTime'])
            item['infoSource'] = chc(item['infoSource'])
            item['infoDetailRaw'] = chc(item['infoDetailRaw'])
            item['infoDetailText'] = h2t.handle(item['infoDetailRaw'])
            item['infoDetailRaw'] = ""     #原始数据太多，测试时清空 
            item['company']['introduction'] = h2t.handle(chc(item['company']['introduction']))
            item['company'] = dict(item['company']) 

            return item

        if spider.name == "CJLU":
            item['title'] = chc(item['title'])
            item['infoDetailRaw'] = chc(item['infoDetailRaw'])
            item['infoDetailText'] = h2t.handle(item['infoDetailRaw'])
            item['infoDetailRaw'] = ""     #原始数据太多，测试时清空 

            return item

        if spider.name == "ZJUT":
            item['title'] = chc(item['title'])
            item['infoDetailRaw'] = chc(item['infoDetailRaw'])
            item['infoDetailText'] = h2t.handle(item['infoDetailRaw'])
            item['infoDetailRaw'] = ""     #原始数据太多，测试时清空 

            return item

        if spider.name == "HZNU":
            item['title'] = chc(item['title'],1)
            item['location'] = chc(item['location'])
            item['startTime'] = chc(item['startTime'])
            item['infoDetailRaw'] = chc(item['infoDetailRaw'])
            item['infoDetailText'] = h2t.handle(item['infoDetailRaw'])
            item['infoDetailRaw'] = ""     #原始数据太多，测试时清空 
            item['company']['introduction'] = h2t.handle(chc(item['company']['introduction']))
            item['company'] = dict(item['company']) 

            return item

        if spider.name == "ZJU":
            item['title'] = chc(item['title'])
            item['location'] = chc(item['location'])
            item['startTime'] = chc(item['startTime'])
            item['infoDetailRaw'] = chc(item['infoDetailRaw'])
            item['infoDetailText'] = h2t.handle(item['infoDetailRaw'])
            item['infoDetailRaw'] = ""     #原始数据太多，测试时清空 
            item['company']['introduction'] = h2t.handle(chc(item['company']['introduction']))
            item['company'] = dict(item['company']) 

            return item

class JsonPipeline(object):

    def __init__(self):
        self.newItem = []

    def open_spider(self, spider):
        self.file = codecs.open(spider.name+'.json','a',encoding='utf-8')

    def process_item(self, item, spider):
        self.newItem.append(item['title']+'_'+item['sid'])

        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + "\n"
        self.file.write(line)
        return item

    def close_spider(self,spider):
        self.file.close()

        #记录spider的新增项目
        fname = os.path.join(os.path.abspath(os.path.dirname(__file__)),"spiders/"+spider.name+"Done")
        f = codecs.open(fname, 'a', 'utf-8')
        for i in self.newItem:
            f.write(i+os.linesep)
        f.close()


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return 'full/%s' % (image_guid)

    def get_media_request(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok,x in results if ok]
        if not image_path:
            raise DropItem("Item contains no images")
        return item

