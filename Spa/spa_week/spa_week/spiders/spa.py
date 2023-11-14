import scrapy
import pandas as pd
from scrapy import Request
import os
from spa_week.items import SpaWeekItem
class SpaSpider(scrapy.Spider):
    name = 'spa'
    allowed_domains = ['www.spaweek.com']
    urls = []
    for page in range(1, 201, 1):
        urls.append("https://www.spaweek.com/spas?gc=1&location=100000&page={}".format(page))
        
    start_urls =  urls   
    # start_urls = ['https://www.spaweek.com/spas?gc=1&location=100000&page=101']
    
    def start_requests(self):
            handle_httpstatus_list = [403]
            headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
            for url in self.start_urls:
                yield Request(url,callback=self.parse ,headers=headers)
    def parse(self, response):
        list_href = response.xpath("//div[@class='row product-pages grid-masonry']//a/@href").extract()
        list_href = list(set(list_href))
        if '' in list_href:
            list_href.remove('')
        
        for i in list_href:
            item = SpaWeekItem()
            item['url'] = i
            yield item
        # print(len(list_href))
        # print(list_href)
