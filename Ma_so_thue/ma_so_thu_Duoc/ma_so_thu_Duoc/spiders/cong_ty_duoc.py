import scrapy
import pandas as pd
from scrapy import Request
import os

class CongTyDuocSpider(scrapy.Spider):
    name = 'cong_ty_duoc'
    allowed_domains = ['masothue.com']
    
    url = []
    for page in range(1, 11, 1):
        url.append('https://masothue.com/tra-cuu-ma-so-thue-theo-nganh-nghe/dich-vu-tam-hoi-massage-va-cac-dich-vu-tang-cuong-suc-khoe-tuong-tu-tru-hoat-dong-the-thao-9610?page={}'.format(page))
    start_urls = url
    # start_urls = ['https://masothue.com/tra-cuu-ma-so-thue-theo-nganh-nghe/dich-vu-tam-hoi-massage-va-cac-dich-vu-tang-cuong-suc-khoe-tuong-tu-tru-hoat-dong-the-thao-9610?page=2']
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
            
    def parse(self, response):
        for nb in range(1, 26,1):
            company_name = response.xpath("//div[@class='container']/div[@class='tax-listing']/div[{}]/h3/a/text()".format(nb)).extract_first()
            mst = response.xpath("//div[@class='container']/div[@class='tax-listing']/div[{}]/div/a/text()".format(nb)).extract_first()
            company_representative = response.xpath("//div[@class='container']/div[@class='tax-listing']/div[{}]/div/em/a/text()".format(nb)).extract_first()
            address = response.xpath("//div[@class='container']/div[@class='tax-listing']/div[{}]/address/text()".format(nb)).extract_first()
            url = response.xpath("//div[@class='container']/div[@class='tax-listing']/div[{}]/h3/a/@href".format(nb)).extract_first()
            dict_result = { 'company_name': company_name,
                            'mst': mst,
                            'company_representative': company_representative,
                            'address': address,
                            'href' : 'https://masothue.com' + url
                            }
            data = pd.DataFrame([dict_result])
            # print(dict_result)
            # data.to_csv("/Users/dinhvan/Projects/Code/crawl/scrapy/ma_so_thu_Duoc/ma_so_thu_Duoc/spiders/duoc_raw.csv", index = False)
            path = '/Users/dinhvan/Projects/Code/web_scrape/scrapy/Ma_so_thue/ma_so_thu_Duoc/ma_so_thu_Duoc/spiders/9610.csv'
            data.to_csv(path, mode='a', header=not os.path.exists(path), index=False)

        
