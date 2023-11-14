import scrapy
import scrapy
from scrapy import Request
from spa_awards.items import SpaAwardsItem
class SpaSpider(scrapy.Spider):
    name = 'spa'
    allowed_domains = ['www.luxuryspaawards.com']
    urls =[]
    for page in range(1,83,1):
        urls.append('https://www.luxuryspaawards.com/find-a-spa/page/{}/'.format(page))
    start_urls = urls
    # start_urls = ['https://www.luxuryspaawards.com/find-a-spa/page/81/']
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
    def parse(self, response):
        list_link = response.xpath("//li[@class='searchbox-result']/a/@href").extract()
        for value in list_link:
            item = SpaAwardsItem()
            item['url'] = value
            yield item
