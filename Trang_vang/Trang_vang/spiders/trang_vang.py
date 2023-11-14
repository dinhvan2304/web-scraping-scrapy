import scrapy
from scrapy import Request
import pandas as pd
import os
from Trang_vang.items import TrangVangItem
class TrangVangSpider(scrapy.Spider):
    name = 'trang_vang'
    allowed_domains = ['www.yellowpages.vn']
    start_url = []
    for page in range(1,3,1):
        start_url.append('https://www.yellowpages.vn/cls/488893/spa-thiet-bi-spa.html?page={}'.format(page)) 
    start_urls = start_url
    # start_urls = ["https://www.yellowpages.vn/cls/488893/spa-thiet-bi-spa.html"]
    
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
            
    def parse(self, response):
        names = response.xpath("//div[@class='listing_box']/div[@class='listing_head']/div[@class='company_name_section']/h2[@class='company_name']/a/text()").extract()
        number_value = len(names)
        for result in range(1,number_value+1,1):
            dict_temp = {'name' : (response.xpath("//div[@class='listing_box'][{}]/div[@class='listing_head']/div[@class='company_name_section']/h2[@class='company_name']/a/text()".format(result)).extract_first()),
                         'address' : (response.xpath("//div[@class='listing_box'][{}]/div[@class='company_content']/div[@class='listing_logo_dc']/div[@class='listing_diachi_tel_email']/p[@class='listing_diachi'][1]/text()".format(result)).extract_first()) if not None else "" + (response.xpath("//div[@class='listing_box'][{}]/div[@class='company_content']/div[@class='listing_logo_dc']/div[@class='listing_diachi_tel_email']/p[@class='listing_diachi'][1]/em/strong/text()".format(result)).extract_first()) if not None else "",
                         'city' : (response.xpath("//div[@class='listing_box'][{}]/div[@class='company_content']/div[@class='listing_logo_dc']/div[@class='listing_diachi_tel_email']/p[@class='listing_diachi'][1]/em/strong/text()".format(result)).extract_first()),
                         'phone_number' : (response.xpath("//div[@class='listing_box'][{}]/div[@class='company_content']/div[@class='listing_logo_dc']/div[@class='listing_diachi_tel_email']/p[@class='listing_tel']/text()".format(result)).extract_first()) ,
                        #  'business_email' : email[result].strip()
                        'type_name' : 'Công ty cung cấp thiết bị spa'
                         }
            
            item = TrangVangItem()
            item['name'] = dict_temp['name']
            item['address'] = dict_temp['address']
            item['city'] = dict_temp['city']
            item['phone_number'] = dict_temp['phone_number']
            # item['business_email'] = dict_temp['business_email']
            item['type_name'] = dict_temp['type_name']
            yield item  
        
            