# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import os
import platform
#from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
import careerTalk.settings as ST
from careerTalk.customUtil import CustomUtil
writeDone = CustomUtil.writeDoneSet
getBase = CustomUtil.getBaseDir
from careerTalk.customUtil import  DoneSet
from scrapy.exceptions import DropItem
chc = CustomUtil.convertHtmlContent



class ItemPipeline(object):
    def process_item(self, item, spider):
    	return CustomUtil.handleItem(item)


class JsonPipeline(object):
    def __init__(self):
        self.itemIds = []
        self.file = None

    def open_spider(self, spider):
        baseDir = getBase()
        fileName = os.path.join(baseDir,spider.name+'.json')
        self.file = codecs.open(fileName,'a',encoding='utf-8')

    def process_item(self, item, spider):
        self.itemIds.append(DoneSet.getItemId(spider, item))

        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()
        writeDone(spider.name+"Done", self.itemIds)


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

