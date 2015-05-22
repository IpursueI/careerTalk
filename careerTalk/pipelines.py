# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import html2text
import json
import codecs
import os
from careerTalk.customUtil import CustomUtil
chc = CustomUtil.convertHtmlContent


class ItemPipeline(object):
    def process_item(self, item, spider):
        if spider.name == "NJU":
            item['university'] = chc(item['university'])
            item['title'] = chc(item['title'])
            item['issueTime'] = chc(item['issueTime'],1)
            item['location'] = chc(item['location'])
            item['startTime'] = chc(item['startTime'])
            item['infoSource'] = chc(item['infoSource'])
            h2t = html2text.HTML2Text()
            h2t.ignore_links = True
            item['infoDetail'] = h2t.handle(chc(item['infoDetail']))
            return item
        if spider.name == "NJUST":
            h2t = html2text.HTML2Text()
            h2t.ignore_links = True
            h2t.ignore_images = True
            item['university'] = chc(item['university'])
            item['title'] = chc(item['title'])
            item['location'] = chc(item['location'])
            item['startTime'] = chc(item['startTime'])
            item['infoSource'] = chc(item['infoSource'])
            item['infoDetail'] = h2t.handle(chc(item['infoDetail']))
            item['companyInfo'] = h2t.handle(chc(item['companyInfo']))

            return item
            

class JsonPipeline(object):

    def __init__(self):
        self.newItem = []

    def open_spider(self, spider):
        self.file = codecs.open(spider.name+'.json','a',encoding='utf-8')

    def process_item(self, item, spider):
        self.newItem.append(item['title'])

        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
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

