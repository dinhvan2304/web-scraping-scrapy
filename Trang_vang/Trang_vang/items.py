# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy import Item
from scrapy import Field

class TrangVangItem(Item):
    type_name = Field()
    name = Field()
    address = Field()
    city = Field()
    phone_number = Field()
    # business_email = Field()
 