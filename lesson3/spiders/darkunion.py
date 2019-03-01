# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest, Request

class DarkunionSpider(scrapy.Spider):
    name = 'darkunion'
    # allowed_domains = ['dark']
    start_urls = ['http://almvdkg6vrpmkvk4.onion/']
    post_data = {
        "username": "alexandrite",
        "password": "almvdkg6vrpmkvk4",
        "login": "登录",
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
            yield scrapy.Request(url, callback=self.parse_login, headers=self.header, 
            # meta={'proxy': '127.0.0.1:8118'}
            )
    
    def parse_login(self, response):
        
        autim = response.xpath('//*[@name="autim"]/@value')[0]
        print(autim)
        sid = response.xpath('//*[@name="sid"]/@value')[0]
        print(sid)
        self.post_data['autim'] = autim
        self.post_data['sid'] = sid
        return FormRequest.from_response(
            response,
            formdata=self.post_data,
            callback=self.parse_after,
            headers=self.header,
        )
        # print(sid)
        # hint = response.xpath('//h1/text()').extract()
        # print(hint)
        # if 'Sorry' in hint:
        #     print('NONONNNNNNNNNNNNNNOOOOOOOOOOOOOOOOOOO')
        # else:
        #     print('YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
    def parse_after(self, response):
        f = open('web.html', 'w')
        f.write(response.text)
        f.close()