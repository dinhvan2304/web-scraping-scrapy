# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field,Item

class SapoItem(Item):
    ten = Field()
    dia_chi = Field()
    hotline = Field()
    website = Field()
