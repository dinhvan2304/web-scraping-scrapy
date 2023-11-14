# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BogiaoducItem(scrapy.Item):
    ten_truong = scrapy.Field()
    loai_hinh = scrapy.Field()
    co_quan = scrapy.Field()
    ky_hieu = scrapy.Field()
    ten_tienganh = scrapy.Field()
    website = scrapy.Field()
    tinh = scrapy.Field()
    loai_truong = scrapy.Field()
