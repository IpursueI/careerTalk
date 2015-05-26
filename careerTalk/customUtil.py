#-*- coding:utf-8 -*-

import json
import re
import html2text
import os
import codecs
from scrapy import log


class CustomUtil(object):
    # 时间格式 2015-03-27 14:00
    time_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})'
    # 日期格式 2015-03-24
    date_pattern = r'(\d{4}-\d{2}-\d{2})'
    
    @staticmethod
    def convertHtmlContent(li, idx=0):
        if len(li) == 0:
            return None
        else:
            return li[idx].strip()

    @staticmethod
    def readLastTime(fileName, item):
        f = file(fileName)
        s = json.load(f)
        f.close()
        return s[item]

    @staticmethod
    def getFirstStr(strs):
        """
        获取字符串列表中的第一个字符串，若获取失败，则返回一个空字符串
        若strs本身是一个字符串，则返回字符串
        """
        isString = isinstance(strs, basestring)
        if isString:
            return strs
        try:
            return strs[0]
        except:
            return ""

    @staticmethod
    def get_matchs(pattern, text):
        ts = []
        it = re.finditer(pattern, text)
        for m in it:
            if m:
                ts.append(m.group())
        return ts

    @classmethod
    def get_times(cls, text):
        """
        获取字符串中的时间
        """
        return cls.get_matchs(cls.time_pattern, text)

    @classmethod
    def get_date(cls, text):
        """
        获取字符串中的日期
        """
        return cls.get_matchs(cls.date_pattern, text)

    @classmethod
    def h2t(cls, html):
        if html:
            ht = html2text.HTML2Text()
            ht.ignore_links = True
            return ht.handle(html)
        return None


class DoneSet(object):
    """
    用于管理各个spider已完成的数据集
    """
    doneSets = {}

    @classmethod
    def getSet(cls, spider):
        key = spider.get('name')
        if not key:
            log.ERROR(spider.__name__ + u' 尚未设置spider.name，获取doneset失败')
            return None
        val = cls.datasets.get(key)
        if val:
            return val
        else:
            return cls.createSetByDoneFile(spider)

    @classmethod
    def createSetByDoneFile(cls, spider):
        """
        通过spiderName创建对应的doneset
        :param spiderName: spider名
        :return: doneset
        """
        # 从文本读取已获取的数据
        filePath = cls.getDonFilePath(spider)
        doneset = set()
        try:
            f = codecs.open(filePath, 'r', 'utf-8')
            for line in f:
                doneset.add(line.strip())
            f.close()
        except:
            log.ERROR(u'读取'+filePath+u'失败')
        return doneset

    @classmethod
    def isInDoneSet(cls, spider, item):
        """
        判断是否需要继续对item进行解析
        :param spider: spider
        :param item: item
        :return: True if the item is not in  doneset
        """
        doneset = cls.getSet(spider)
        id = cls.getItemId(spider, item)
        return doneset.__contains__(id)

    @classmethod
    def getItemId(cls, spider, item):
        """
        :return: 根据item信息返回一个用于区分不同item的字符串
        """
        sid = item.get('sid')
        title = item.get('title')
        startTime = item.get('startTime')
        if title and sid:
            return sid+'_'+title
        elif title and startTime:
            return startTime+'_'+title
        else:
            log.WARNING('can not get the itemId , item:'+str(item))
            return item.__hash__

    @classmethod
    def createDoneFile(cls, spider, keys):
        filePath = cls.getDonFilePath(spider)
        dir = os.path.dirname(filePath)
        if not os.path.exists(dir):
            os.mkdir(dir)
        file = codecs.open(filePath, 'a', encoding='utf-8')
        for key in keys:
            file.write(key+os.linesep)
        file.close()
        return filePath


    @classmethod
    def getDonFilePath(cls, spider):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), "../test/"+spider.name+"/Done")

