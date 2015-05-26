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
        'careerTalk.pipelines.MyImagesPipeline':850,
        }

DOWNLOAD_TIMEOUT = 15
IMAGES_STORE = '/home/captain/文档/program/python/careerTalk/picture'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'careerTalk (+http://www.yourdomain.com)'
