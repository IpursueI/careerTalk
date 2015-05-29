# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import html2text
import json
import codecs
import os
from careerTalk.customUtil import CustomUtil, DoneSet
from scrapy.exceptions import DropItem
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
        # todo 需要删除
        # if item.get('infoDetailRaw'):
        #     item['infoDetailRaw'] = None

        # 如果标题为空，则采用公司名替换，若公司名也不存在，则直接抛弃
        if not item.get('title'):
            if item.get('company') and item.get('company').get('name'):
                item['title'] = item['company']['name']
            else:
                raise DropItem("Missing title and companyName in %s" % item)
        return item

    def process_item_SEU(self, item, spider):
        if item.get('targetMajor'):
            item['targetMajor'] = chc(item['targetMajor'])
        if item.get('targetAcademic'):
            item['targetAcademic'] = chc(item['targetAcademic'])
        return item


class JsonPipeline(object):
    def __init__(self):
        self.itemIds = []
        self.file = None

    def open_spider(self, spider):
        fname = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../test/"+spider.name+"/data.json")
        dir = os.path.dirname(fname)
        if not os.path.exists(dir):
            os.mkdir(dir)
        self.file = codecs.open(fname, 'a', encoding='utf-8')

    def process_item(self, item, spider):
        self.itemIds.append(DoneSet.getItemId(spider, item))

        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + "\n,"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()
        DoneSet.createDoneFile(spider, self.itemIds)

