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
    
    # def __init__(self, host, database, user, password, port):
    #     self.host = host
    #     self.database = database
    #     self.user = user
    #     self.password = password
    #     self.port = port
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         host=crawler.setting.get('MYSQL_HOST'),
    #         database=crawler.setting.get('MYSQL_DATABASE'),
    #         user=crawler.setting.get('MYSQL_USER'),
    #         password=crawler.setting.get('MYSQL_PASSWORD'),
    #         port=crawler.setting.get('MYSQL_PORT'),
    #     )
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DATABASE','images')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '123qwe')
        self.db_conn =pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()
        # self.db_conn = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf-8', port=self.port)
        # self.cursor = self.db.cursor()
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()
    def process_item(self, item, spider):
        self.insert_db(item)
        return item
    def insert_db(self, item):
        values = (
            item['title'],
            item['url'],
            item['thumb'],
            # item['review_rating'],
            # item['review_num'],
            # item['stock'],
        )
        sql = 'INSERT INTO images VALUES(%s,%s,%s)'
        self.db_cur.execute(sql, values)