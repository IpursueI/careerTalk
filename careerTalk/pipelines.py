# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import os
<<<<<<< HEAD
import platform
#from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
import careerTalk.settings as ST
from careerTalk.customUtil import CustomUtil
writeDone = CustomUtil.writeDoneSet
getBase = CustomUtil.getBaseDir
=======
import careerTalk.settings as ST
from careerTalk.customUtil import CustomUtil, DoneSet
from scrapy.exceptions import DropItem
chc = CustomUtil.convertHtmlContent
>>>>>>> dev-phk


class ItemPipeline(object):
    def process_item(self, item, spider):
<<<<<<< HEAD
    	return CustomUtil.handleItem(item)
=======
        # todo 暂时不显示infodetailraw
        if item['infoDetailRaw']:
            item['infoDetailRaw'] = None
        # todo 暂时不做html转text处理
        # if item['infoDetailRaw']:
        #     h2t = html2text.HTML2Text()
        #     h2t.ignore_links = True
        #     item['infoDetailText'] = h2t.handle(chc(item['infoDetailRaw']))
        #     return item
>>>>>>> dev-phk

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


class JsonPipeline(object):
    def __init__(self):
        self.itemIds = []
        self.file = None

    def open_spider(self, spider):
<<<<<<< HEAD
        baseDir = getBase()
        fileName = os.path.join(baseDir,spider.name+'.json')
        self.file = codecs.open(fileName,'a',encoding='utf-8')

    def process_item(self, item, spider):
        self.newItem.append(item['title']+'_'+item['sid'])

        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + "\n"
=======
        storePath = ST.MY_SETTING['STORE_PATH'] or os.path.abspath(os.path.dirname(__file__))+"/../test/"
        fname = os.path.join(storePath, spider.name+"/data.json")
        target_dir = os.path.dirname(fname)
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        self.file = codecs.open(fname, 'a', encoding='utf-8')

    def process_item(self, item, spider):
        self.itemIds.append(DoneSet.getItemId(spider, item))

        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + "\n,"
>>>>>>> dev-phk
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()
<<<<<<< HEAD
        writeDone(spider.name+"Done", self.newItem)


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
=======
        DoneSet.createDoneFile(spider, self.itemIds)
>>>>>>> dev-phk

