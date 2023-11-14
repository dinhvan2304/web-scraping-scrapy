import scrapy
from scrapy import Request
import pandas as pd
import numpy as np
import os

class VuongBaoSpider(scrapy.Spider):
    name = 'vuong_bao'
    allowed_domains = ['vuongbao.vn']
    start_urls = ['https://vuongbao.vn/diem-ban/danh-sach-dai-ly-nha-thuoc-phan-phoi-tai-vinh-long/']
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
    def parse(self, response):
        location = response.xpath("//main[@class='content']/article[@class='post-1583 page type-page status-publish entry']/div[@class='entry-content']/h2[@class='sub_dist_title']/text()").getall()
        # print(location)
        if len(location) > 0:
            for lct in range(len(location)):
                location_result = response.xpath("//table[@class='diem_ban layout_3col'][{}]//td[@class='dia_chi']/text()".format(lct+1)).getall()
                name_result = response.xpath("//table[@class='diem_ban layout_3col'][{}]//td[@class='ten_nha_thuoc']/text()".format(lct+1)).getall()
                phone_number_result = response.xpath("//table[@class='diem_ban layout_3col'][{}]//td[@class='sdt']/a/text()".format(lct+1)).getall()
                
                number = len(location_result)
                for nb in range(number):
                    dict_split = {
                        'location_result': location_result[nb],
                        'name_result' : name_result[nb],
                        'phone_number_result' : phone_number_result[nb],
                        'district' : location[lct]
                    }
                    print(dict_split)
                    result = pd.DataFrame([dict_split])
                    path_result = "/Users/dinhvan/Projects/Code/crawl/scrapy/Vuong_bao/Vuong_bao/spiders/result.csv"
                    result.to_csv(path_result, mode='a', header=not os.path.exists(path_result), index = False)
        else:
            pass
        
        
        