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
            item['title'] = chc(item['title'])
            item['issueTime'] = chc(item['issueTime'],1)
            h2t = html2text.HTML2Text()
            h2t.ignore_links = True
            item['infoDetail'] = h2t.handle(chc(item['infoDetail']))
            return item
        if spider.name == 'SEU':
            return self.process_item_SEU(item, spider)
        if item.get('company'):
            item['company'] = dict(item['company'])
        # todo需要删除
        if item.get('infoDetailRaw'):
            item['infoDetailRaw'] = None
        return item

    def process_item_SEU(self, item, spider):
        if item.get('targetMajor'):
            item['targetMajor'] = chc(item['targetMajor'])
        if item.get('targetAcademic'):
            item['targetAcademic'] = chc(item['targetAcademic'])
        return item


class JsonPipeline(object):
    items = []
    def __init__(self):
        self.newItem = []

    def open_spider(self, spider):
        fname = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../test/"+spider.name+"/data.json")
        dir = os.path.dirname(fname)
        if not os.path.exists(dir):
            os.mkdir(dir)
        self.file = codecs.open(fname, 'a', encoding='utf-8')

    def process_item(self, item, spider):
        if item.get('sid'):
            self.newItem.append(item['title']+"_"+item['sid'])
        else:
            self.newItem.append(item['title'])
        # line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # self.file.write(line)
        JsonPipeline.items.append(dict(item))
        return item

    def close_spider(self,spider):
        line = json.dumps(JsonPipeline.items, ensure_ascii=False)
        self.file.write(line)
        self.file.close()

        #记录spider的新增项目
        fname = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../test/"+spider.name+"/Done.md")
        f = codecs.open(fname, 'a', 'utf-8')
        for i in self.newItem:
            f.write(i+os.linesep)
        f.close()

