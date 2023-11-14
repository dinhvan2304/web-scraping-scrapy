import scrapy
from scrapy import Request
import pandas as pd
from nha_thuoc.items import NhaThuocItem
class NhaThuoc1Spider(scrapy.Spider):
    name = 'nha_thuoc_1'
    allowed_domains = ['imiale.com']

    url_data = pd.read_csv('/Users/dinhvan/Projects/Code/web_scraping/scrapy/nha_thuoc/href.csv', dtype = str)
    url = url_data['href'].values.tolist()
    start_urls = url
    # start_urls = ['https://imiale.com/ba-dinh/']
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
    
    def parse(self, response):
        count = len(response.xpath("//table/tbody//td[1]").extract())
        for i in range(2,count+2,1):
            # dict_temp = {   
            #             'name': response.xpath("//table//tr[{}]/td[1]/text()".format(i)).extract_first(),
            #             'location' : response.xpath("//table//tr[{}]/td[2]/text()".format(i)).extract_first()
            #             }
            result = NhaThuocItem()
            result['name'] = response.xpath("//table//tr[{}]/td[1]/text()".format(i)).extract_first()
            result['location'] = location = " ".join(response.xpath('//table//tr[{}]/td[2]/text()'.format(i)).extract())
            yield result
            
        
