# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest, Request
import urllib
from lesson3.items import OnionItem
import time, random, os
class DarkunionSpider(scrapy.Spider):
    name = 'spider_10006'
    # allowed_domains = ['dark']
    start_urls = ['http://almvdkg6vrpmkvk4.onion/']
    post_data = {
        "username": "phosphophyllite",
        "password": "Phosphophyllite3.5",
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
        
        autim = response.xpath('//*[@name="autim"]/@value').extract()
        print(autim)
        sid = response.xpath('//*[@name="sid"]/@value').extract()
        print(sid)
        self.post_data['autim'] = autim
        self.post_data['sid'] = sid
        return FormRequest.from_response(
            response,
            formdata=self.post_data,
            callback=self.parse_after,
            headers=self.header,
        )
        
    def parse_after(self, response):
        f = open('web.html', 'w')
        index_url =  response.xpath('//*[contains(@class,"text_index_top")]//@href').extract()
        index_title =  response.xpath('//*[contains(@class,"text_index_top")]/text()').extract()
        
        base_url = response.url
        for url in index_url:
            f.write(url + '\r\n')
            if 'q_ea_id' in url and int(url.split('=')[-1]) == 10006:
                aera_url = urllib.parse.urljoin(base_url, url)
                
                yield scrapy.Request(aera_url, callback=self.parse_page, headers=self.header)
        f.close()
    
    def parse_page(self, response):
        base_url = response.url        
        topic_url = response.xpath('//a[text()="打开"]/@href').extract()                
        for url in topic_url:
            # f = open('topic', 'a')
            time.sleep(5 + round(random.random()*5,1))
            # f.write('*****************************************************\r\n')
            # f.write(urllib.parse.urljoin(base_url, url) + '\r\n')
            # f.close()
            yield scrapy.Request(urllib.parse.urljoin(base_url, url), callback=self.parse_item, headers=self.header)           

    def parse_item(self, response):
        # print('*********************************')
        # print(response.url)
        time.sleep(5 + round(random.random()*5,1))
        self.location = time.strftime("%Y-%m-%d", time.localtime())
        self.existorcreate()
        cwd = os.getcwd()              
        trade_id = response.xpath('//td[text()="交易编号:"]/following::*[1]/text()').extract()[0]
        # filename = item['trade_id']
        f = open(cwd + os.sep + self.location + os.sep + trade_id, 'w')
        f.write(response.text)
        f.close()

    def existorcreate(self):
        if not self.location:
            self.location = 'temp'
        if not os.path.exists(self.location):
            os.mkdir(self.location)           