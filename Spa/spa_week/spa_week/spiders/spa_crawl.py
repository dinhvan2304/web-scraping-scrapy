import scrapy
import pandas as pd
from scrapy import Request
import os
from spa_week.items import SpaWeekCrawlItem
class SpaCrawlSpider(scrapy.Spider):
    name = 'spa_crawl'
    allowed_domains = ['www.spaweek.com']
    
    df_href = pd.read_csv("/Users/dinhvan/Projects/Code/web_scraping/scrapy/Spa/spa_week/spa_week/spiders/href.csv", dtype = str)
    start_urls = df_href['url'].values.tolist()
    start_urls = start_urls[6300:6600]
    # start_urls = ['https://www.spaweek.com/spa/30198/jeanne-marie-auger-holistic-health-practitioner']
    def start_requests(self):
            handle_httpstatus_list = [403]
            headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
            for url in self.start_urls:
                yield Request(url,callback=self.parse ,headers=headers)
    def parse(self, response):
        item = SpaWeekCrawlItem()
        item['name'] = response.xpath("//h1/text()").extract_first()
        item['phone'] = response.xpath("//div[@class='right-side']/div[@id='contact-d']/ul/li[@class='ip']/text()").extract_first()
        item['address'] = response.xpath("//div[@class='overview-content'][2]/div[@class='location']/text()").extract_first()
        item['web'] = response.xpath("//div[@class='right-side']/div[@id='contact-d']/ul/li[@class='web']/a/@href").extract_first()
        # item['menu'] = response.xpath("//div[@id='menuSpa']/div[@class='menu-acc text-center']/div[@class='acc-list']/div[@class='acc-heading accordion act']/text()").extract_first()
        yield item
