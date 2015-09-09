# -*- coding: utf-8 -*-

# Scrapy settings for careerTalk project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'careerTalk'

SPIDER_MODULES = ['careerTalk.spiders']
NEWSPIDER_MODULE = 'careerTalk.spiders'

ITEM_PIPELINES = { 
        'careerTalk.pipelines.ItemPipeline':300,
        'careerTalk.pipelines.JsonPipeline':800,
        #'careerTalk.pipelines.MyImagesPipeline':850,
        }

DOWNLOAD_TIMEOUT = 15

MY_SETTING={
        'version':1,
        # 'STORE_PATH':None
        'STORE_PATH': "/home/phk52/server/scrapyd/data/",
        'STORE_PATH_WINDOWS': "E:\code\python\careerTalkData"
}

IMAGES_STORE = 'E:\code\python\careerTalkData\picture'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'careerTalk (+http://www.yourdomain.com)'
