import scrapy
from scrapy import Request
from spa_index.items import SpaIndexItem
class SpaSpider(scrapy.Spider):
    name = 'spa'
    allowed_domains = ['www.spaindex.com']
    urls =[]
    for page in range(1,5,1):
        urls.append('https://www.spaindex.com/listings/category/spas-usa/page/{}/'.format(page))
    start_urls = urls
    # start_urls = ['https://www.spaindex.com/listings/category/spas-usa/page/1/']
    
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
    
    def parse(self, response):
        list_link = response.xpath("//div[@id='content-mid']/div[@id='content-inner']/div[@class='list']//h2[@class='entry-title']/a/@href").extract()
        description = response.xpath("//div[@class='list']//div[3]/p[@class='listing-description']/text()").extract()
        for link in range(200):
            item = SpaIndexItem()
            
            item['url'] = list_link[link]
            item['description'] = description[link]
            
            yield item
            
