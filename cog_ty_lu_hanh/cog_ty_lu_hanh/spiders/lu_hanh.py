import scrapy
from scrapy import Request
import pandas as pd
from cog_ty_lu_hanh.items import CogTyLuHanhItem
class LuHanhSpider(scrapy.Spider):
    name = 'lu_hanh'
    allowed_domains = ['www.quanlyluhanh.vn']
    urls =[]
    for page in range(1,164,1):
        urls.append('https://www.quanlyluhanh.vn/index.php/cat/1020/{}'.format(page))
    start_urls = urls
    # start_urls = ['https://www.quanlyluhanh.vn/index.php/cat/1001/200']
    
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)

    
    def get_dict(self, list_raw):
        keys = ['address','business_license_number','license_date', 'phone_number', 'email' , 'website', 'operating_range']
        dict_value = dict.fromkeys(keys)
        for value in list_raw:
            if 'Địa điểm kinh doanh:' in value or 'Địa chỉ:' in value:
                dict_value['address'] = value.replace('Địa điểm kinh doanh: ','').replace('Địa chỉ: ','')
            if 'Giấy phép kinh doanh lữ hành số:' in value:
                dict_value['business_license_number'] = value.replace('Giấy phép kinh doanh lữ hành số: ','') 
            if 'Ngày cấp:' in value:
                dict_value['license_date'] = value.replace('Ngày cấp: ','')
            if 'Email:' in value:
                dict_value['email'] = value.replace('Email: ','')
            if 'Website:' in value:
                dict_value['website'] = value.replace('Website: ','')
            if 'Điện thoại:' in value:
                dict_value['phone_number'] = value.replace('Điện thoại: ','')
            if 'Phạm vi hoạt động:' in value:
                dict_value['operating_range'] = value.replace('Phạm vi hoạt động: ','')
                
        return dict_value
            
    def parse(self, response):
            
        for nb in range(1,11,1):
            list_raw = (response.xpath("//div[@class='col-md-8 left padd-top background1 padd-bot']/div[@class='col-md-12 left background']/div[@class='full left']/div[@class='full left thick-border'][{}]/div[@class='col-md-12']/ul[@class='other-info']/li[@class='info']//text()".format(nb)).extract())
            list_raw = [i.strip() for i in list_raw]
            
            address = self.get_dict(list_raw)['address']
            if address is not None:
                address = address.replace('\n','').replace('\t','').replace('\r','')
                
            item = CogTyLuHanhItem()
            item['company_name'] = response.xpath("//div[@class='col-md-8 left padd-top background1 padd-bot']/div[@class='col-md-12 left background']/div[@class='full left']/div[@class='full left company-name mar-bot'][{}]/div[@class='full tendn bold upper-case']//text()".format(nb)).extract_first()
            item['company_name_el'] = response.xpath("//div[@class='col-md-8 left padd-top background1 padd-bot']/div[@class='col-md-12 left background']/div[@class='full left']/div[@class='full left company-name mar-bot'][{}]/div[@class='full tengiaodich bold upper-case']//text()".format(nb)).extract_first()
            item['address'] = address
            item['business_license_number'] = self.get_dict(list_raw)['business_license_number']
            item['license_date'] = self.get_dict(list_raw)['license_date']
            item['email'] = self.get_dict(list_raw)['email']
            item['website'] = self.get_dict(list_raw)['website']
            item['phone_number'] = self.get_dict(list_raw)['phone_number']
            item['operating_range'] = self.get_dict(list_raw)['operating_range']
            yield item

