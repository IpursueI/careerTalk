#-*- coding:utf-8 -*-

import json
import re

class CustomUtil(object):
    # 时间格式 2015-03-27 14:00
    time_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2})')
    # 日期格式 2015-03-24
    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')
    
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
