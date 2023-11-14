import scrapy
from scrapy import Request
import pandas as pd
import numpy as np
import os

class SpaSpider(scrapy.Spider):
    name = 'spa'
    allowed_domains = ['www.tripadvisor.com.vn']
    start_urls = ['https://www.tripadvisor.com.vn/Attractions-g293921-Activities-c40-Vietnam.html']
    
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
            
    def parse(self, response):
        # list_url = response.xpath("//section[@class='jemSU']/div[@class='BqDzz z']/div[@class='C']/div[@class='C']/div/article[@class='GTuVU XJlaI']/div[@class='hZuqH']/header[@class='VLKGO']/div[@class='NxKBB']/div/div[@class='alPVI eNNhq PgLKC tnGGX']/a[1]/h3[@class='biGQs _P fiohW ngXxk']/div[@class='ATCbm']/span/div[@class='XfVdV o AIbhI']/text()").extract()
        # print(list_url)
        print(1)