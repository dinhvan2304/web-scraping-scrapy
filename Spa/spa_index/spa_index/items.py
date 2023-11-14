# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class SpaIndexItem(scrapy.Item):
    url = Field()
    description = Field()
    
class SpaCrawlItem(scrapy.Item):
    name = Field()
    listed_in = Field()
    address = Field()
    phone = Field()
    web = Field()
    link_face = Field()
    link_twitter = Field()
    url = Field()

