#-*- coding:utf-8 -*-

import json

class CustomUtil(object):
    
    @staticmethod
    def convertHtmlContent(li, idx=0):
        isString = isinstance(li, basestring)
        if isString:
            return li
        else:
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
