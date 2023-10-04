# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class SpaAwardsItem(scrapy.Item):
    url = Field()

class SpaAwardsItemDetail(scrapy.Item):
    name = Field()
    country = Field()
    address = Field()
    phone = Field()
    facebook = Field()
    instagram = Field()
    twitter = Field()
    pinterest = Field()
    web = Field()
