# -*- coding: utf-8 -*-
import scrapy


class DarkunionSpider(scrapy.Spider):
    name = 'darkunion'
    # allowed_domains = ['dark']
    start_urls = ['http://22222222jpg4oobq.onion/']
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
            yield scrapy.Request(url, callback=self.parse, headers=self.header, 
            # meta={'proxy': '127.0.0.1:8118'}
            )
    def parse(self, response):
        f = open('web.html', 'w')
        f.write(response.text)
        f.close()
        # hint = response.xpath('//h1/text()').extract()
        # print(hint)
        # if 'Sorry' in hint:
        #     print('NONONNNNNNNNNNNNNNOOOOOOOOOOOOOOOOOOO')
        # else:
        #     print('YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')