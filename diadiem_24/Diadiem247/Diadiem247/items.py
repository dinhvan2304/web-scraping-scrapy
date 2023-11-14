# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class Diadiem247Item(scrapy.Item):
    name = Field()
    phone_number = Field()
    location = Field()
    fb_link = Field()
    web_link = Field()
    email = Field()
    url = Field()
