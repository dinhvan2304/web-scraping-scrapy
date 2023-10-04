import scrapy
from scrapy import Request
import pandas as pd
from hotel.items import HotelItem

class Hotel2StarSpider(scrapy.Spider):
    name = 'hotel_2_star'
    allowed_domains = ['csdl.vietnamtourism.gov.vn']
    urls =[]
    for page in range(1,7,1):
        urls.append('http://csdl.vietnamtourism.gov.vn/tt?page={}'.format(page))
    start_urls = urls
    # start_urls = ['https://csdl.vietnamtourism.gov.vn/cslt/?csrf_name=5deca45d6104ed8074cd85b84c684718&type%5B0%5D=1&page=470']
    
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)

    def get_dict(self, list_raw):
        # keys = ['hotel_name', 'type_hotel', 'address', 'number_room', 'landline_phone', 'email' , 'website' ,'mobile_phone', 'fax', 'status', 'price']
        keys = ['gym_name', 'address', 'landline_phone','mobile_phone']
        dict_value = dict.fromkeys(keys)
        # dict_value['hotel_name'] = list_raw[0]
        dict_value['gym_name'] = list_raw[0]
        # dict_value['type_hotel'] = list_raw[1]
        # dict_value['status'] = list_raw[-1]
        for value in list_raw:
            if 'Địa chỉ:' in value:
                dict_value['address'] = value.replace('Địa chỉ: ','')
            if 'Số phòng:' in value:
                dict_value['number_room'] = value.replace('Số phòng: ','')
            if 'Giá:' in value:
                dict_value['price'] = value.replace('Giá: ','')
            if 'Điện thoại cố định:' in value:
                dict_value['landline_phone'] = value.replace('Điện thoại cố định: ','')
            if 'Email:' in value:
                dict_value['email'] = value.replace('Email: ','')
            if 'Fax:' in value:
                dict_value['fax'] = value.replace('Fax: ','')
            if 'Website:' in value:
                dict_value['website'] = value.replace('Website: ','')
            if 'Điện thoại di động:' in value:
                dict_value['mobile_phone'] = value.replace('Điện thoại di động: ','')
                
        return dict_value
            
    def parse(self, response):
        for nb in range(1,16,1):
            list_raw = (response.xpath("//div[@class='col-lg-8']/div[@class='row'][2]/div[@class='col-lg-12 col-md-12 col-sm-12 h-100'][{}]/div[@class='verticleilist listing-shot']/div[@class=' cslt-items row mx-0']/div[@class='col-md-12 h-100 pt-3']/div[@class='verticle-listing-caption']//text()".format(nb)).extract())
            if len(list_raw) != 0:
                list_raw = [vl.strip() for vl in list_raw]
                list_raw = [i for i in list_raw if i]
            
                item = HotelItem()
                # item['hotel_name'] = self.get_dict(list_raw)['hotel_name']
                # item['type_hotel'] = self.get_dict(list_raw)['type_hotel']
                # item['address'] = self.get_dict(list_raw)['address']
                # item['number_room'] = self.get_dict(list_raw)['number_room']
                # item['landline_phone'] = self.get_dict(list_raw)['landline_phone']
                # item['email'] = self.get_dict(list_raw)['email']
                # item['website'] = self.get_dict(list_raw)['website']
                # item['mobile_phone'] = self.get_dict(list_raw)['mobile_phone']
                # item['fax'] = self.get_dict(list_raw)['fax']
                # item['status'] = self.get_dict(list_raw)['status']
                # item['price'] = self.get_dict(list_raw)['price']

                item['gym_name'] = self.get_dict(list_raw)['gym_name']
                item['address'] = self.get_dict(list_raw)['address']
                item['landline_phone'] = self.get_dict(list_raw)['landline_phone']
                item['mobile_phone'] = self.get_dict(list_raw)['mobile_phone']
                
                yield item
            
            