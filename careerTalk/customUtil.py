#-*- coding:utf-8 -*-

import json
import re
import platform
import os
import codecs
import careerTalk.settings as ST
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