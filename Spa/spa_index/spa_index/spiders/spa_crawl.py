import scrapy
from scrapy import Request
import pandas as pd
from spa_index.items import SpaCrawlItem

class SpaCrawlSpider(scrapy.Spider):
    name = 'spa_crawl'
    allowed_domains = ['www.spaindex.com']
    
    df_link = pd.read_csv("link.csv", dtype = str)
    start_urls = df_link['url'].values.tolist()
    # start_urls = ['https://www.spaindex.com/listings/kabuki-springs-spa-sf/']
    
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
            
    def parse(self, response):
        name = response.xpath("//h1[@class='entry-title']/a/text()").extract_first()
        listed_in = response.xpath("//div[@id='main']//p[1]/a/text()").extract()
        listed_in = ', '.join(x for x in listed_in)
        address = response.xpath("//div[@id='main']//div[2]/ul/li[@class='address']/text()").extract_first()
        phone = response.xpath("//div[@id='main']//div[2]/ul/li[@class='phone']/strong/text()").extract_first()
        web  = response.xpath("//div[@id='main']//div[2]/ul/li[@id='listing-website']/a/text()").extract_first()
        link_face = response.xpath("//div[@id='main']//div[@id='listing-follow']/a[1]/@href").extract_first()
        link_twitter = response.xpath("//div[@id='main']//div[@id='listing-follow']/a[2]/@href").extract_first()
        url = response.request.url 
        
        result = SpaCrawlItem()
        result['name'] = name
        result['listed_in'] = listed_in
        result['address'] = address
        result['phone'] = phone
        result['web'] = web
        result['link_face'] = link_face
        result['link_twitter'] = link_twitter
        result['url'] = url
        
        yield result
        

        