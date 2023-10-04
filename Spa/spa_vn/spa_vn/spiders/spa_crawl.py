import scrapy
import pandas as pd
from scrapy import Request
import os

class SpaCrawlSpider(scrapy.Spider):
    name = 'spa_crawl'
    allowed_domains = ['www.tripadvisor.com.vn']
    df_link = pd.read_csv("/Users/dinhvan/Projects/Code/web_scraping/selenium/spa_link.csv", dtype = str)
    start_urls = df_link['url'].values.tolist()
    start_urls = ['https://www.tripadvisor.com.vn/Attraction_Review-g293925-d26338593-Reviews-Rosie_Monday_Wellness_Spa-Ho_Chi_Minh_City.html']
    
    def start_requests(self):
            headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
            for url in self.start_urls:
                yield Request(url,callback=self.parse ,headers=headers)
                
    def parse(self, response):
        spa_name = response.xpath("//h1[@class='biGQs _P fiohW eIegw']/text()").extract_first()
        # address = response.xpath("//div[@class='IjjLa']/div[@class='wgNTK']/div[@class='MJ']/button[@class='UikNM _G B- _S _T c G_ y wSSLS wnNQG raEkE']/span[@class='biGQs _P XWJSj Wb']/text()").extract_first()
        
        # list_contact = response.xpath("//div[@class='IuzAT e']/div[@class='aVUMb'][2]/div[@class='WoBiw Q3 K']/a[@class='UikNM _G B- _S _T c G_ y bYExr wnNQG raEkE']/@href").extract()
        
        # print(list_contact)    
        print(spa_name)
