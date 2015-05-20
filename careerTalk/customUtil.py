#-*- coding:utf-8 -*-

class CustomUtil(object):
    
    @staticmethod
    def convertHtmlContent(li, idx=0):
        if len(li) == 0:
            return None
        else:
            return li[idx].strip()

