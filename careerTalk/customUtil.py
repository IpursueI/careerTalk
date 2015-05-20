#-*- coding:utf-8 -*-

import json

class CustomUtil(object):
    
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
