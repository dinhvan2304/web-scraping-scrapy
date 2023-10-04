# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class CogTyLuHanhItem(scrapy.Item):
    company_name = Field()
    company_name_el = Field()
    address= Field()
    business_license_number = Field()
    license_date = Field()
    email = Field()
    website = Field()
    phone_number = Field()
    operating_range = Field()