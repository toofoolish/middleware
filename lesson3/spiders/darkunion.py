# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest, Request
import urllib
from lesson3.items import OnionItem
import time, random, os
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
        # for i in range(len(index_title)):
        #     f.write(index_title[i] + ' ==> ' + index_url[i] + '\r\n')
        
        base_url = response.url
        for url in index_url:
            if 'q_ea_id' in url and int(url.split('=')[-1]) < 20000:
                aera_url = urllib.parse.urljoin(base_url, url)
                f.write(aera_url + '\r\n')
                yield scrapy.Request(aera_url, callback=self.parse_page, headers=self.header)
        f.close()
    def parse_page(self, response):
        base_url = response.url        
        topic_url = response.xpath('//a[text()="打开"]/@href').extract()                
        for url in topic_url:
            f = open('topic', 'a')
            time.sleep(round(random.random()*2,1))
            f.write('*****************************************************\r\n')
            f.write(urllib.parse.urljoin(base_url, url) + '\r\n')
            f.close()
            yield scrapy.Request(urllib.parse.urljoin(base_url, url), callback=self.parse_item, headers=self.header)
        
        # next_page_sel = response.xpath('//button[contains(@class,"page_b2")]')[-1]
        next_page = response.xpath('//button[contains(@class,"page_b2")]/following::a[1]/@href').extract()
        if next_page:
            # f = open('pages', 'a')
            next_url = urllib.parse.urljoin(base_url, next_page[-1])
            # print('***********************')
            # print(next_url)
            # f.write(next_url + '\r\n')
            # f.close()
            time.sleep(3 + round(random.random()*5,1))
            yield scrapy.Request(next_url, callback=self.parse_page, headers=self.header)               

    def parse_item(self, response):
        # print('*********************************')
        # print(response.url)
        time.sleep(3 + round(random.random()*5,1))
        self.location = time.strftime("%Y-%m-%d", time.localtime())
        self.existorcreate()
        cwd = os.getcwd()
        
        item = OnionItem()
        item['trade_id'] = response.xpath('//td[text()="交易编号:"]/following::*[1]/text()').extract()[0]
        # filename = item['trade_id']
        f = open(cwd + os.sep + self.location + os.sep + item['trade_id'], 'w')
        f.write(response.text)
        f.close()
        item['sold_num'] = response.xpath('//td[text()="本单成交:"]/following::*[1]/text()').extract()[0]
        post_time = response.xpath('//p[contains(@class, "author")]/text()').extract()[-1].strip()
        yy = post_time[:4]
        mm = post_time.split('-')[1][:-1]
        if len(mm) == 1:
            mm = '0' + mm
        dd = post_time.split('-')[-1][:2]
        tt = post_time.split(':')[0][-2:]
        ff = post_time.split(':')[1].rstrip()
        # print(yy+mm+dd+tt+ff+'00')
        item['post_time'] = yy+mm+dd+tt+ff+'00'
        item['area'] = response.xpath('//*[contains(@class,"link_blue")]/text()').extract()[1].strip()
        item['username'] = response.xpath('//td[text()="账户名称:"]/following::*[1]/text()').extract()[0]
        item['userid'] = response.xpath('//td[text()="账户编号:"]/following::*[1]/text()').extract()[0]
        reg_time = response.xpath('//dd[contains(@class, "profile-joined")]/text()').extract()[0].strip()
        yy = reg_time[:4]
        mm = reg_time.split('-')[1][:-1]
        if len(mm) == 1:
            mm = '0' + mm
        dd = reg_time.split('-')[-1][:2]
        tt = reg_time.split(':')[0][-2:]
        ff = reg_time.split(':')[1].rstrip()
        item['reg_time'] = yy+mm+dd+tt+ff+'00'
        item['title'] = response.xpath('//*[contains(@class,"first")]/a/text()').extract()[0]
        item['price'] = response.xpath('//*[contains(@class,"t_2")]/text()').extract()[-1]
        lines = response.xpath('//div[contains(@class,"content")]/text()').extract()
        content = ''.join(lines).strip()
        item['content'] = content.replace('\n', '')
        # # item['content'] = response.xpath('//div[contains(@class,"content")]/text()').extract()
        # # item['reader'] = topic.xpath('/td[7]/text()')
        # print('***********************\r\n')
        # for i in item:
        #     print(i + ' ==>> ' + item[i] + '\r\n')
        # print('***********************\r\n')
        return item
    def existorcreate(self):
        if not self.location:
            self.location = 'temp'
        if not os.path.exists(self.location):
            os.mkdir(self.location)           