# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import MapCompose, Join
import urllib
import socket
import datetime
from lesson3.items import Lesson3Item
from scrapy import FormRequest
class EasySpider(CrawlSpider):
    name = 'login'
    def start_requests(self):
        return [
            FormRequest(
                "http://127.0.0.1:9312/dynamic/login",
                formdata={"user": "user", "pass": "pass"},
                
            )
        ]

    def parse_item(self, response):
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