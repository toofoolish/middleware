# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from lesson3.db.dbhelper import DBHelper

class Lesson3Pipeline(object):
    def process_item(self, item, spider):
        return item

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name
    
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item
    
    def get_media_requests(self, item, info):
        yield Request(item['url'])

class MysqlPipeline():
    def open_spider(self, spider):
        self.db = pymysql.connect("localhost","test","123qwe","tot" )
        self.cursor = self.db.cursor()
        # self.db_conn = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf-8', port=self.port)
        # self.cursor = self.db.cursor()
    def close_spider(self, spider):
        
        self.db.close()
    def process_item(self, item, spider):
        values = (
            item['trade_id'],
            item['sold_num'],
            item['post_time'],
            item['area'],
            item['username'],
            item['userid'],
            item['reg_time'],
            item['title'],
            item['price'],
            item['content'],
        )
        sql = "insert into forum(trade_id, sold_num, \
                post_time, area, username, userid, reg_time, title, price, content) \
                values (%s, %s,  '%s',  '%s',  '%s', %s, '%s', '%s', %s, '%s')" 
        try:
            self.cursor.execute(sql % values)
            self.db.commit()
            print('save to mysql!')
        except:
            self.db.rollback()
            print('Failed to save!')

class topicpipeline():
    def open_spider(self, spider):
        self.file = open('item', 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        for i in item:
            self.file.write(i + ' ==> ' + item[i] + '\r\n')