import scrapy
import pandas as pd
from scrapy import Request
from Drugs.items import DrugsItem

class DrugSpider(scrapy.Spider):
    name = 'drug'
    allowed_domains = ['www.drugs.com']
    start_urls = ['http://www.drugs.com/']
    url = pd.read_csv('/Users/dinhvan/Projects/Code/crawl/selenium/Drugs/url.csv', dtype = str)
    start_urls = url['url'].to_list()
    # start_urls = ['https://www.drugs.com/manufacturer/ironwood-pharmaceuticals-inc-568.html']
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
    def parse(self, response):
        name = response.xpath("//main[@id='container']/div[@id='contentWrap']/div[@id='content']/div[@class='contentBox']/h1/text()").extract_first()
        phone_number = response.xpath("//div[@id='contentWrap']/div[@id='content']/div[@class='contentBox']/div[@class='ddc-manufacturer-details']/p/span[1]/text()").extract_first()
        website = response.xpath("//div[@id='contentWrap']/div[@id='content']/div[@class='contentBox']/div[@class='ddc-manufacturer-details']/p/span[2]/a/text()").extract_first()
        list_description = response.xpath("//div[@id='contentWrap']/div[@id='content']/div[@class='contentBox']/div[@class='ddc-manufacturer-details']/p/text()").extract()
        description = ' '.join(list_description)
        description = description.replace('\r\n','')
        dict_temp = {'name': name,
                     'phone_number': phone_number,
                     'website' : website,
                     'description': description}
        # print(dict_temp)
        result = DrugsItem()
        result['name'] = dict_temp['name']
        result['phone_number'] = dict_temp['phone_number']
        result['website'] = dict_temp['website']
        result['description'] = dict_temp['description']
        yield result