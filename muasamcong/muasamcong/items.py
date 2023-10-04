# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MuasamcongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    # so_TBMT = scrapy.Field()
    thoi_diem_dang_tai = scrapy.Field()
    thoi_diem_nhan_EHSDT = scrapy.Field()
    thoi_diem_dong_mo = scrapy.Field()
    den_ngay = scrapy.Field()
    pass
