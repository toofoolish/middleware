# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class Lesson3Item(Item):
    # define the fields for your item here like:
    title = Field()
    price = Field()
    description = Field()
    address = Field()
    image_urls = Field()

    images = Field()
    location = Field()

    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()

class ImageItem(Item):
    collection = table = 'images'
    id = Field()
    url = Field()
    title = Field()
    thumb = Field()