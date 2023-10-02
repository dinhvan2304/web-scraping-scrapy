import scrapy
from scrapy import Request
import pandas as pd
class FdiSpiderSpider(scrapy.Spider):
    name = 'FDI_spider'
    allowed_domains = ['masothue.com']
    list_result = []
    df = pd.DataFrame()
    start_urls = [
    'https://masothue.com/tra-cuu-ma-so-thue-theo-loai-hinh-doanh-nghiep/doanh-nghiep-100-von-dau-tu-nuoc-ngoai-9?page=1',
    'https://masothue.com/tra-cuu-ma-so-thue-theo-loai-hinh-doanh-nghiep/doanh-nghiep-100-von-dau-tu-nuoc-ngoai-9?page=2',
    'https://masothue.com/tra-cuu-ma-so-thue-theo-loai-hinh-doanh-nghiep/doanh-nghiep-100-von-dau-tu-nuoc-ngoai-9?page=3',
    'https://masothue.com/tra-cuu-ma-so-thue-theo-loai-hinh-doanh-nghiep/doanh-nghiep-100-von-dau-tu-nuoc-ngoai-9?page=4',
    'https://masothue.com/tra-cuu-ma-so-thue-theo-loai-hinh-doanh-nghiep/doanh-nghiep-100-von-dau-tu-nuoc-ngoai-9?page=5',
    'https://masothue.com/tra-cuu-ma-so-thue-theo-loai-hinh-doanh-nghiep/doanh-nghiep-100-von-dau-tu-nuoc-ngoai-9?page=6',
    'https://masothue.com/tra-cuu-ma-so-thue-theo-loai-hinh-doanh-nghiep/doanh-nghiep-100-von-dau-tu-nuoc-ngoai-9?page=7',
    'https://masothue.com/tra-cuu-ma-so-thue-theo-loai-hinh-doanh-nghiep/doanh-nghiep-100-von-dau-tu-nuoc-ngoai-9?page=8',
    'https://masothue.com/tra-cuu-ma-so-thue-theo-loai-hinh-doanh-nghiep/doanh-nghiep-100-von-dau-tu-nuoc-ngoai-9?page=9',
    'https://masothue.com/tra-cuu-ma-so-thue-theo-loai-hinh-doanh-nghiep/doanh-nghiep-100-von-dau-tu-nuoc-ngoai-9?page=10',
    ]
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
    def parse(self, response):
        result = response.xpath("//main[@id='main']/section[@class='animate-in-view fadeIn animated']/div[@class='container']/div[@class='tax-listing']/div/div/a/text()").getall()
        self.list_result = self.list_result + result
        df = pd.DataFrame(self.list_result)
        df.to_csv('mst.csv')
