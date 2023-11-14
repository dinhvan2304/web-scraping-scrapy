import scrapy
from scrapy import Request
import pandas as pd
import os
from Diadiem247.items import Diadiem247Item

class Diadiem247Spider(scrapy.Spider):
    name = 'diadiem247'
    allowed_domains = ['diadiem247.com']
    url_df = pd.read_csv("/Users/dinhvan/Projects/Code/crawl/selenium/dia_diem_247/link.csv", dtype = str)
    list_url = url_df['url'].values.tolist()
    start_urls = list_url
    # start_urls = ['https://diadiem247.com/ha-noi/waxing-house-hanoi-dalink-spa--l369622.html']
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,
                          callback=self.parse,
                          headers=headers
                          )
    def deCFEmail(self,fp):
        try:
            r = int(fp[:2],16)
            email = ''.join([chr(int(fp[i:i+2], 16) ^ r) for i in range(2, len(fp), 2)])
            return email
        except (ValueError):
            return None
        
    def parse(self, response):
        # fp = '3a4d5b4253545d52554f495f4c547a5d575b535614595557'
        # print(self.deCFEmail(fp))
        
        name = response.xpath("//div[@class='col-md-8']/h1/text()").extract_first()
        phone_number = response.xpath("//div[@class='location_info']/a/text()").extract_first()
        location = (response.xpath("//div[@class='location_info'][2]/text()").extract()[1]).replace('\n','')
        fb_link = response.xpath('//a[contains(@data-original-title, "Facebook")]/@href').extract_first()
        web_link = response.xpath('//a[contains(@data-original-title, "Website")]/@href').extract_first()
        email_code = response.xpath('//a[contains(@data-original-title, "Email")]/@href').extract_first()
        if email_code is not None:
            email_code = (email_code.split("#"))[1]
            email = self.deCFEmail(email_code)
        else:
            email = None
        url  = response.url
    
        result = Diadiem247Item()
        result['name'] = name
        result['phone_number'] = phone_number
        result['location'] = location
        result['fb_link'] = fb_link
        result['web_link'] = web_link
        result['email'] = email
        result['url'] = url
        
        if ((phone_number is None) or ('x' in phone_number) or ('Gọi điện thoại' in phone_number) or ('Đang cập nhật' in phone_number)) and email is None:
            pass
        else:
            yield result
        