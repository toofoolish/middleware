# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest, Request
import urllib
from lesson3.items import OnionItem
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
        # print(sid)
        # hint = response.xpath('//h1/text()').extract()
        # print(hint)
        # if 'Sorry' in hint:
        #     print('NONONNNNNNNNNNNNNNOOOOOOOOOOOOOOOOOOO')
        # else:
        #     print('YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')/html/body/div/div[2]/div/table[2]/tbody/tr[4]
    def parse_after(self, response):
        f = open('web.html', 'w')
        index_url =  response.xpath('//*[contains(@class,"text_index_top")]//@href').extract()
        index_title =  response.xpath('//*[contains(@class,"text_index_top")]/text()').extract()
        for i in range(len(index_title)):
            f.write(index_title[i] + ' ==> ' + index_url[i] + '\r\n')
        f.close()
        base_url = response.url
        for url in index_url:
            if 'q_ea_id' in url:
                aera_url = urllib.parse.urljoin(base_url, url)
                yield scrapy.Request(aera_url, callback=self.parse_page, headers=self.header)
    
    def parse_page(self, response):
        page_num = response.xpath('//*[contains(@class,"page_b1")][-1]/text()').extract()
        
        base_url = response.url
        if page_num and page_num != 1:
            for page in range(2, page_num + 1):
                url = base_url + '&pagey=' + str(page) + '#pagey'
                yield scrapy.Request(url, callback=self.parse_item, headers=self.header)

    def parse_item(self, response):
        table = response.xpath('//*[contains(@class,"m_area_a")]/tbody/tr')
        for topic in table:
            
