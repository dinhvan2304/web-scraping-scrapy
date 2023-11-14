# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item

class DichvucongItem(scrapy.Item):
    stt = Field()
    ma_ho_so = Field()
    thong_tin = Field()
    href = Field()
    so_cong_bo = Field()
    ten_doanh_nghiep = Field()
    ten_TTBYT = Field()
    trang_thai = Field()