# -*- coding: utf-8 -*-
import scrapy
import datetime
# import urlparse
import urllib
import socket
from lesson3.items import Lesson3Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join

class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['web']
    start_urls = ['http://127.0.0.1:9312/properties/property_000003.html',]
    

    def parse(self, response):
        # item = Lesson3Item()
        # item['title'] = response.xpath('//*[@itemprop="name"][1]/text()').extract()
        # item['price'] = response.xpath('//*[@itemprop="price"][1]/text()').re('[.0-9]+')
        # item['description'] = response.xpath('//*[@itemprop="description"][1]/text()').extract()
        # item['address'] = response.xpath('//*[@itemtype="http://schema.org/Place"][1]/text()').extract()
        # item['image_urls'] = response.xpath('//*[@itemprop="image"][1]/@src').extract()
        # self.log('title: %s' % response.xpath('//*[@itemprop="name"][1]/text()').extract())
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
        l.add_value('project', self.settings.get('BOT_NAME  '))
        return l.load_item()
