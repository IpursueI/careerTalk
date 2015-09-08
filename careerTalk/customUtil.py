#-*- coding:utf-8 -*-

import json
import re
class CustomUtil(object):

    @staticmethod
    def convertHtmlContent(li, idx=0):
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