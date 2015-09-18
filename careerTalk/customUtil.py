#-*- coding:utf-8 -*-

import json
import re
import platform
import os
import codecs
from scrapy import log
import time
import html2text
import careerTalk.settings as ST
class CustomUtil(object):

    # 时间格式 2015-03-27 14:00
    time_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})'
    time_format = "%Y-%m-%d %H:%M"
    # 日期格式 2015-03-24
    date_pattern = r'(\d{4}-\d{2}-\d{2})'

    @staticmethod
    def convertHtmlContent(li, idx=0):

        if li is None:
            return ""
        isString = isinstance(li, basestring)
        if isString:
            return li
        else:
            if len(li) == 0:
                return ""
            else:
                return li[idx].strip()

    @staticmethod
    def readLastTime(fileName, item):
        f = file(fileName)
        s = json.load(f)
        f.close()
        return s[item]

    @staticmethod
    def phoneNumberRegular(content):
        phonePre = ['134','135','136','137','138','139','147','150','151','152','157','158','159','182','183','184','187','188','178',
                    '130','131','132','155','156','185','186','145','176',
                    '133','153','180','189','177']
        regular = '|'.join(['('+i+'\d{8}'+')' for i in phonePre])
        tPhoneNumber = re.findall(regular+u'|(\d{4}-|\d{3}-)(\d{8}|\d{7})|(\d{4}\u2014|\d{3}\u2014)(\d{8}|\d{7})|(8\d{7})',content)
        return " ".join([''.join(i) for i in tPhoneNumber])

    @staticmethod
    def emailRegular(content):
        tEmail = re.findall('[\w+\.]*\w+-*\w+@\w+[\.com|\.org|\.cn]+',content)
        return " ".join(tEmail) if tEmail else ""

    @staticmethod
    def getBaseDir():
        if platform.system() == 'Linux':
            return ST.MY_SETTING['STORE_PATH']
        if platform.system() == 'Windows':
            return ST.MY_SETTING['STORE_PATH_WINDOWS']

    @staticmethod
    def getDoneSet(fileName):
        baseDir = CustomUtil.getBaseDir()
        DoneFile = os.path.join(baseDir,fileName)
        if not os.path.exists(DoneFile):
            open(DoneFile,'w')
        Done = set()
        f = codecs.open(DoneFile,'r','utf-8')
        for line in f:
            Done.add(line.strip())
        f.close()
        return Done

    @staticmethod
    def writeDoneSet(fileName, newItem):
        baseDir = CustomUtil.getBaseDir()
        DoneFile = os.path.join(baseDir,fileName)
        f = codecs.open(DoneFile, 'a', 'utf-8')
        for i in newItem:
            f.write(i+os.linesep)
        f.close()

    @staticmethod
    def handleItem(item):
        h2t = html2text.HTML2Text()
        h2t.ignore_links = True
        h2t.ignore_images = True

        item['university'] = CustomUtil.convertHtmlContent(item.get('university',''))
        item['title'] = CustomUtil.convertHtmlContent(item.get('title',''))
        item['issueTime'] = CustomUtil.convertHtmlContent(item.get('issueTime',''))
        item['startTime'] = CustomUtil.convertHtmlContent(item.get('startTime',''))
        item['location'] = CustomUtil.convertHtmlContent(item.get('location',''))
        item['infoSource'] = CustomUtil.convertHtmlContent(item.get('infoSource',''))
        item['infoDetailRaw'] = CustomUtil.convertHtmlContent(item.get('infoDetailRaw',''))
        item['infoDetailText'] = h2t.handle(item['infoDetailRaw'])
        item['infoDetailRaw'] = "" #infoDetailRaw 数据量大，暂时清空
        item['link'] = CustomUtil.convertHtmlContent(item.get('link',''))
        item['sid'] = CustomUtil.convertHtmlContent(item.get('sid',''))
        item['company']['name'] = CustomUtil.convertHtmlContent(item['company'].get('name',''))
        item['company']['introduction'] = h2t.handle(CustomUtil.convertHtmlContent(item['company'].get('introduction','')))
        item['company']['phoneNumber'] = CustomUtil.phoneNumberRegular(item['infoDetailText']) + CustomUtil.phoneNumberRegular(item['company']['introduction'])
        item['company']['email'] = CustomUtil.emailRegular(item['infoDetailText']) + CustomUtil.emailRegular(item['company']['introduction'])
        item['company'] = dict(item['company']) 
        
        return item

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

    @classmethod
    def splitTimes(cls, timeStr):
        """
        解析时间串，获取起始时间与结束时间
        2015-4-21 13:30—15:30
        """
        timeStr = timeStr.strip()
        # 替换中文空格
        timeStr = timeStr.replace(u'\xa0', ' ')
        # 替换空白字符
        timeStr = timeStr.replace('\r', ' ')
        # 替换中文冒号
        timeStr = timeStr.replace(u'：', ':')
        # 替换中文破折号
        timeStr = timeStr.replace(u'——', '-')
        timeStr = timeStr.replace(u'—', '-')
        timeStr = timeStr.replace(u'\u2014', '-')

        t_format = r"(\d{4}-\d{1,2}-\d{1,2})\s+(\d{1,2}:\d{1,2})[-|\s|~]*(\d{1,2}:\d{1,2})?"
        st = None
        et = None

        m = re.search(t_format, timeStr)
        if m:
            date = m.group(1)
            tst = m.group(2)
            tet = m.group(3)
            if date:
                if tst:
                    st = time.strptime(date+' '+tst, CustomUtil.time_format)
                    st = time.strftime(CustomUtil.time_format, st)
                if tet:
                    et = time.strptime(date+' '+tet, CustomUtil.time_format)
                    et = time.strftime(CustomUtil.time_format, et)
        return st, et,


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
        # filePath = cls.getDonFilePath(spider)
        # doneset = set()
        # try:
        #     f = codecs.open(filePath, 'r', 'utf-8')
        #     for line in f:
        #         doneset.add(line.strip())
        #     f.close()
        # except:
        #     log.msg(u'读取'+filePath+u'失败', level=log.WARNING, spider=spider)
        # return doneset
        return CustomUtil.getDoneSet(spider.name)

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
        # sid = item.get('sid')
        # title = item.get('title')
        # startTime = item.get('startTime')
        # if sid:
        #     if title:
        #         return sid+'_'+title
        #     else:
        #         return sid+'_'
        # elif title and startTime:
        #     return startTime+'_'+title
        # else:
        #     log.msg('can not get the itemId , item:'+str(item), level=log.WARNING, spider=spider)
        #     return item.__hash__()
        return item['title']+'_'+item['sid']

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

    # @classmethod
    # def getDonFilePath(cls, spider):
    #     storePath = ST.MY_SETTING['STORE_PATH'] or os.path.abspath(os.path.dirname(__file__))+"/../test/"
    #     return os.path.join(storePath, spider.name+"/Done.txt")
