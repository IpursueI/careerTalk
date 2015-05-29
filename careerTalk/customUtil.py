#-*- coding:utf-8 -*-

import json
import re
import html2text
import os
import codecs
from scrapy import log
import time


class CustomUtil(object):
    # 时间格式 2015-03-27 14:00
    time_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})'
    time_format = "%Y-%m-%d %H:%M"
    # 日期格式 2015-03-24
    date_pattern = r'(\d{4}-\d{2}-\d{2})'
    
    @staticmethod
    def convertHtmlContent(li, idx=0):
        if li is None or len(li) == 0:
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
    def formatTime(cls, time_str):
        t_format = r"\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}"
        if re.match(t_format, time_str):
            timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M")
            format_time = time.strftime(cls.time_format, timeArray)
            return format_time
        return time_str


    @classmethod
    def strip(cls, str):
        if isinstance(str, basestring):
            return str.strip()
        return str

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
        key = spider.name
        if not key:
            log.msg(spider.__name__ + u' 尚未设置spider.name，获取doneset失败', level=log.ERROR, spider=spider)
            return None
        val = cls.doneSets.get(key)
        if val is not None:
            return val
        else:
            s = cls.createSetByDoneFile(spider)
            cls.doneSets[key] = s
            return s

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
            log.msg(u'读取'+filePath+u'失败', level=log.WARNING, spider=spider)
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
        if sid:
            return sid+'_'+title
        elif title and startTime:
            return startTime+'_'+title
        else:
            log.msg('can not get the itemId , item:'+str(item), level=log.WARNING, spider=spider)
            return item.__hash__()

    @classmethod
    def createDoneFile(cls, spider, keys):
        filePath = cls.getDonFilePath(spider)
        dir = os.path.dirname(filePath)
        if not os.path.exists(dir):
            os.mkdir(dir)
        file = codecs.open(filePath, 'a', encoding='utf-8')
        for key in keys:
            # print key
            file.write(key+os.linesep)
        file.close()
        if len(keys):
            log.msg((spider.name+u'新添加了%d个数据,起始点为 '+keys[0]) % len(keys), level=log.INFO, spider=spider)
        else:
            log.msg(spider.name+u'未添加新数据', level=log.INFO, spider=spider)
        return filePath

    @classmethod
    def getDonFilePath(cls, spider):
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), "../test/"+spider.name+"/Done.txt")

