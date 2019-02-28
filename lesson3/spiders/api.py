# -*- coding: utf-8 -*-
import scrapy
import datetime
# import urlparse
import urllib
import socket
from lesson3.items import Lesson3Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy import Request
import json
class BasicSpider(scrapy.Spider):
    name = 'api'
    # allowed_domains = ['properties']
    start_urls = ['http://127.0.0.1:9312/properties/api.json',]

    def parse(self, response):
        base_url = "http://127.0.0.1:9312/properties/"
        js = json.loads(response.body)
        for item in js:
            id = item['id']
            url = base_url + 'property_%06d.html' % id
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        # item = Lesson3Item()
        # item['title'] = response.xpath('//*[@itemprop="name"][1]/text()').extract()
        # item['price'] = response.xpath('//*[@itemprop="price"][1]/text()').re('[.0-9]+')
        # item['description'] = response.xpath('//*[@itemprop="description"][1]/text()').extract()
        # item['address'] = response.xpath('//*[@itemtype="http://schema.org/Place"][1]/text()').extract()
        # item['image_urls'] = response.xpath('//*[@itemprop="image"][1]/@src').extract()
        # # self.log('title: %s' % response.xpath('//*[@itemprop="name"][1]/text()').extract())

        # return item
        l = scrapy.loader.ItemLoader(item=Lesson3Item(), response=response)
        l.add_xpath('title', '//*[@itemprop="name"][1]/text()')
        l.add_xpath('price', '//*[@itemprop="price"][1]/text()', MapCompose(lambda i: i.replace(',', ''), float), re='[.0-9]+')
        l.add_xpath('description', '//*[@itemprop="description"][1]/text()', Join())
        l.add_xpath('address', '//*[@itemtype="http://schema.org/Place"][1]/text()')
        l.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src', MapCompose(lambda i: urllib.parse.urljoin(response.url, i)))
        l.add_value('url', response.url)
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())
        l.add_value('project', self.settings.get('BOT_NAME'))
        return l.load_item()
    
    