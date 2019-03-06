# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest, Request
import urllib
from lesson3.items import OnionItem
import time, random
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
        # print('*********************************\r\n')
        # print(topic_url + '\r\n')
        # print('*********************************\r\n')
        
        for url in topic_url:
            f = open('topic', 'a')
            time.sleep(round(random.random()*2,1))
            f.write('*****************************************************\r\n')
            f.write(urllib.parse.urljoin(base_url, url) + '\r\n')
            f.close()
            yield scrapy.Request(urllib.parse.urljoin(base_url, url), callback=self.parse_item, headers=self.header)
        
        next_page = response.xpath('//button[contains(@class,"page_b2")]/following::a[1]/@href').extract()
        if next_page:
            f = open('pages', 'a')
            next_url = urllib.parse.urljoin(base_url, next_page[0])
            f.write(next_url + '\r\n')
            f.close()
            # yield scrapy.Request(next_url, callback=self.parse_page, headers=self.header)
        # next_page = response.xpath('//button[contains(@class,"page_b2")][2]/following::*/button/text()')
        # if next_page:
        #      url = base_url + '&pagey=' + str(next_page) + '#pagey'
        # try:
        #     page_num = response.xpath('//*[contains(@class,"page_b1")]/text()').extract()[-1]
        #     page_num = int(page_num)
            
        #     f = open('pages', 'a')
        #     f.write('*****************************************************\r\n')
        #     if page_num > 1:
        #         for page in range(2, page_num + 1):
        #             url = base_url + '&pagey=' + str(page) + '#pagey'
        #             f.write(url + '\r\n')
        #             # yield scrapy.Request(url, callback=self.parse_page, headers=self.header)
        #     f.close()
        # except:
        #     print(response.url + ' has no more pages!!!')
        

    def parse_item(self, response):
        # l = scrapy.loader.ItemLoader(item=Lesson3Item(), response=response)
        # print('*********************************\r\n')
        # print(response.url + '\r\n')
        # print('*********************************\r\n')
        item = OnionItem()
        # trade_id = Field()
        # sold_num = Field()
        # post_time = Field()
        # area = Field()
        # username = Field()
        # userid = Field()/html/body/div/div[2]/ul/table[2]/tbody/tr[5]/td[2]
        # reg_time = Field()/html/body/div/div[2]/ul/table[2]/tbody/tr[7]/td[2]
        # title = Field()/html/body/div/div[2]/ul/form[1]/table/tbody/tr[3]/td[6]
        # price = Field()
        # content = Field()
        item['trade_id'] = response.url.split('=')[-1]
        item['sold_num'] = response.xpath('//*[contains(@class,"v_table_1")]/tbody//tr[7]/td[4]/text()').extract()[0]
        item['posttime'] = response.xpath('//*[contains(@class,"v_table_1")]/tbody//tr[3]/td[6]/text()').extract()[0]
        item['area'] = response.xpath('//*[contains(@class,"link_blue")]/text()').extract()[1]
        item['username'] = response.xpath('//*[contains(@class,"page_b1")]/text()').extract()[0]
        item['userid'] = response.xpath('//*[contains(@class,"v_table_1")]/tbody//tr[5]/td[2]/text()').extract()[0]
        item['reg_time'] = response.xpath('//*[contains(@class,"v_table_1")]/tbody//tr[7]/td[2]/text()').extract()[0]
        item['title'] = response.xpath('//*[contains(@class,"first")]/text()').extract()[0]
        item['price'] = response.xpath('//*[contains(@class,"t_2")]/text()').extract()[2]
        item['content'] = response.xpath('//*[contains(@class,"content")]/text()').extract()[0]
        # item['reader'] = topic.xpath('/td[7]/text()')
        return item

