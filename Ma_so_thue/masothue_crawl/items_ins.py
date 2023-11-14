# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MasothueCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    province = scrapy.Field()
    province_code = scrapy.Field()
    vi_name = scrapy.Field()
    en_name = scrapy.Field()
    mst = scrapy.Field()
    city = scrapy.Field()
    street = scrapy.Field()
    district = scrapy.Field()
    location = scrapy.Field()
    phone = scrapy.Field()
    telco = scrapy.Field()
    manager_name = scrapy.Field()
    created_date = scrapy.Field()
    main_business = scrapy.Field()
    main_business_code = scrapy.Field()
    enterprise_type = scrapy.Field()
    status = scrapy.Field()
    business = scrapy.Field()

