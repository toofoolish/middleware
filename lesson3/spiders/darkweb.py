# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest, Request
import urllib
from lesson3.items import OnionItem
import time, random
import os
class DarkunionSpider(scrapy.Spider):
    name = 'darkweb'
    # allowed_domains = ['dark']
    start_urls = ['http://22u75kqyl666joi2.onion/ucp.php?mode=login']
    post_data = {
        "username": "alfabeta",
        "password": "22u75kqyl666joi2",
        "login": "登录",
        "redirect": "./index.php?"
    }
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Connection': 'keep-alive',
    }

    def start_requests(self):
        for url in self.start_urls:
            return [
            FormRequest(
                url,
                formdata=self.post_data,
                callback=self.parse_after,
                headers=self.header,
            )
        ]
       
    def parse_after(self, response):
        f = open('web.html', 'w')
        f.write(response.text)
        f.close()
        forum_url = response.xpath('//*[contains(@class,"forumtitle")]/@href').extract()
        for url in forum_url:
            yield scrapy.Request(urllib.parse.urljoin(response.url, url), callback=self.parse_page, headers=self.header)

    def parse_page(self, response):        
        topic_url = response.xpath('//*[contains(@class,"topictitle")]/@href').extract()
        for url in topic_url:
            
            yield scrapy.Request(urllib.parse.urljoin(response.url, url), callback=self.parse_item, headers=self.header)
            
        next_page = response.xpath('//li[contains(@class,"active")]/following::a[1]/@href').extract()
        if next_page:
            
            next_url = urllib.parse.urljoin(response.url, next_page[0])
            yield scrapy.Request(next_url, callback=self.parse_page, headers=self.header)

    def parse_item(self, response):
        print('*********************************')
        print(response.url)
        time.sleep(round(random.random()*2,1))
        self.location = time.strftime("%Y-%m-%d", time.localtime())
        self.existorcreate()
        cwd = os.getcwd()
        filename = response.url.split('=')[-1]
        f = open(cwd + os.sep + self.location + os.sep + filename, 'w')
        f.write(response.text)
        f.close()

    def existorcreate(self):
        if not os.path.exists(self.location):
            os.mkdir(self.location)
