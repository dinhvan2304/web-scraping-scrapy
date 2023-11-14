import scrapy
from scrapy import Request
import pandas as pd
from spa_awards.items import SpaAwardsItemDetail

class SpaDetailSpider(scrapy.Spider):
    name = 'spa_detail'
    allowed_domains = ['www.luxuryspaawards.com']
    
    df_link = pd.read_csv('/Users/dinhvan/Projects/Code/web_scraping/scrapy/spa_awards/spa_awards/spiders/link.csv', dtype = str)
    start_urls = df_link['url'].values.tolist()
    # start_urls = ['https://www.luxuryspaawards.com/spa/anumba-spa/']
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)

    def parse(self, response):
        fb, ig, tt, pr, web = None, None, None, None, None
        list_link = response.xpath("//div[@class='content']/div[@class='social-icon']/a[@class='white']/@href").extract()
        for link in list_link:
            if 'facebook' in link:
                fb = link
            elif 'instagram' in link:
                ig = link
            elif 'twitter' in link:
                tt = link
            elif 'pinterest' in link:
                pr = link
            else :
                web = link
        
        item = SpaAwardsItemDetail()
        
        item['name'] = response.xpath("//div[@class='left']/div[@class='content']/h1[@class='white']/text()").extract_first()
        item['country'] = (response.xpath("//p[@class='meta white hotel-name']/span[@class='golden']/text()").extract_first()).strip()
        item['address'] = response.xpath("//div[@class='contact']/div[@class='table'][1]/div[@class='white meta contact-info']/text()").extract_first()
        item['phone'] = response.xpath("//div[@class='table'][2]/p[@class='white meta contact-info']/a[@class='ph-no']/text()").extract_first()
        item['facebook'] = fb
        item['twitter'] = tt
        item['pinterest'] = pr
        item['instagram'] = ig
        item['web'] = web
        
        yield item
