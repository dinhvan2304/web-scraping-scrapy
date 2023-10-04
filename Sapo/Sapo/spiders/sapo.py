import scrapy
import pandas as pd
from scrapy import Request
import os
from Sapo.items import SapoItem
class SapoSpider(scrapy.Spider):
    name = 'sapo'
    allowed_domains = ['www.sapo.vn']
    
    url = pd.read_csv('/Users/dinhvan/Projects/Code/crawl/scrapy/Sapo/Sapo/source_url.csv', dtype = str)
    start_urls = url['url'].to_list()
    # start_urls = ['https://www.sapo.vn/khach-hang/Phu-Quoc-Bee-Farm']
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
    
    def parse(self, response):
        ten = response.xpath("//div[@class='container']/div[@class='shop-info']/div[@class='row']/div[@class='col-lg-8']/h1/text()").getall()
        
        dia_chi = response.xpath("//div[@class='col-lg-8']/div[@class='row']/div[@class='col-lg-6 item-info'][1]/text()").getall()
        dia_chi.remove(" ") if " " in dia_chi else dia_chi
        
        hotline = response.xpath("//div[@class='col-lg-8']/div[@class='row']/div[@class='col-lg-6 item-info'][2]/text()").getall()
        hotline.remove(" ") if " " in hotline else hotline
        
        # for entry in response.xpath("//div[@class='recipe-description']/a"):
        #     print entry.xpath('href').extract()
        website = response.xpath("//div[@class='col-lg-8']/div[@class='row']/div[@class='col-lg-6 item-info'][3]/a/text()").getall()
        # website.remove(" ") if " " in hotline else hotline
        
        Item = SapoItem()
        Item['ten'] = ten
        Item['dia_chi'] = dia_chi
        Item['hotline'] = hotline
        Item['website'] = website
        
        yield Item
        
        
