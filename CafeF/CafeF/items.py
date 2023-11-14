# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CafefItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    mck_cong_ty_HO = scrapy.Field()
    ten_cong_ty_con = scrapy.Field()
    ti_le_so_huu = scrapy.Field()
    
