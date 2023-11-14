# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class SpaWeekItem(scrapy.Item):
    url = Field()
class SpaWeekCrawlItem(Item):
    name = Field()
    phone = Field()
    address = Field()
    web = Field()
    menu = Field()

