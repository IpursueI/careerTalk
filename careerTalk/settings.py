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

# COOKIES_ENABLES = False
# DOWNLOAD_DELAY = 0.5
# CONCURRENT_REQUESTS_PER_DOMAIN = 6

ITEM_PIPELINES = { 
        'careerTalk.pipelines.ItemPipeline':300,
        'careerTalk.pipelines.JsonPipeline':800,
        }

# 设置json文件存储路径
MY_SETTING={
        'version':1,
        # 'STORE_PATH':None
        'STORE_PATH': "/home/phk52/server/scrapyd/data/"
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'careerTalk (+http://www.yourdomain.com)'

# 取消默认的useragent,使用新的useragent
# DOWNLOADER_MIDDLEWARES = {
#         'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
#         'careerTalk.useragent.RotateUserAgentMiddleware': 400
# }

