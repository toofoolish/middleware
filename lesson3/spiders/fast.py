# -*- coding: utf-8 -*-
import scrapy
import datetime
# import urlparse
import urllib
import socket
from lesson3.items import Lesson3Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
# from scrapy.http import Request

class BasicSpider(scrapy.Spider):
    name = 'fast'
    # allowed_domains = ['properties']
    start_urls = ['http://127.0.0.1:9312/properties/index_00000.html',]

    def parse(self, response):
        next_selector = response.xpath('//*[contains(@class,"next")]//@href')
        # f = open('urls', 'a')
        for url in next_selector.extract():
            # f.write(response.urljoin(url) + '\r\n')
            yield scrapy.Request(response.urljoin(url), callback=self.parse)
        selectors = response.xpath('//*[@itemtype="http://schema.org/Product"]')
        for selector in selectors:
            # f.write(response.urljoin(url) + '\r\n')
            yield self.parse_item(selector, response)
        # f.close()

    def parse_item(self, selector, response):
        
        l = ItemLoader(item=Lesson3Item(), selector=selector)
        l.add_xpath('title', '//*[@itemprop="name"][1]/text()')
        l.add_xpath('price', '//*[@itemprop="price"][1]/text()', MapCompose(lambda i: i.replace(',', ''), float), re='[.0-9]+')
        l.add_xpath('description', '//*[@itemprop="description"][1]/text()', Join())
        l.add_xpath('address', '//*[@itemtype="http://schema.org/Place"][1]/text()')
        l.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src', MapCompose(lambda i: response.urljoin(i)))
        
        l.add_value('url', '//*[@itemprop="url"][1]/@href', MapCompose(lambda i: response.urljoin(i)))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())
        l.add_value('project', self.settings.get('BOT_NAME'))
        return l.load_item()
    
    