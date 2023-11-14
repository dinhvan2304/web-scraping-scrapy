import scrapy
from scrapy import Request
import pandas as pd
from BoGiaoDuc.items import BogiaoducItem

class DaihocCaodangSpider(scrapy.Spider):
    name = 'daihoc_caodang'
    allowed_domains = ['moet.gov.vn']
    list_result = []
    df = pd.DataFrame()
    # start_urls = ['https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=1',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=2',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=3',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=4',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=5',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=6',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=7',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=8',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=9',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=10',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=11',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=12',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=13',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=14',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=15',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=16',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=17',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=18',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=19',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=20',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=21',
    #               'https://moet.gov.vn/cosogiaoduc/Pages/danh-sach.aspx?search=1&field=Title&asc=True&Page=22'
    #               ]
    data = pd.read_csv('/Users/dinhvan/Projects/Code/crawl_data/scrapy/BoGiaoDuc/id_daihoc.csv')
    start_urls = data['id_daihoc'].values.tolist()

    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
            
    def parse(self, response):
        # id = response.xpath("//table[@class='table table-bordered tbl-lich']//td[@class='td-duongdan']/a/@href").getall()
        # for i in id:
        #     self.list_result = self.list_result + id
        #     # header = ['index','id']
        #     df = pd.DataFrame(self.list_result,)
        #     df = df.drop_duplicates(keep='first', ignore_index= True)
        #     df.to_csv('id_daihoc.csv')
        list_keys = []
        list_values = []
        
        key_response = response.xpath("//table[@class='tbl-chitiet']//tr/td[@class='td-lable']/text()").getall()
        list_keys = [key for key in key_response]
        # del list_keys[-3:]
        
        value_response = response.xpath("//table[@class='tbl-chitiet']//tr/td[2]/text() | //table[@class='tbl-chitiet']//tr/td[2]/a/text()").getall()
        list_values = [value for value in value_response]
        # del list_values[-3:]
        print(len(list_values))
        if(len(list_values) == 7):
            list_values.insert(6, None)

        # print(list_values)
        # dict_value = dict(zip(list_keys,list_values))
        # print(dict_value)
        # data = pd.DataFrame(dict_value)
        # df = pd.concat([df, data], ignore_index=True)
        # df.to_csv('daihoc_caodang.csv')
        # item = BogiaoducItem()
        # item['ten_truong'] = dict_value.get("Tên trường")
        # item['loai_hinh'] = dict_value.get("Loại hình cơ sở đào tạo")
        # item['co_quan'] = dict_value.get("Cơ quan quản lý trực tiếp")
        # item['ky_hieu'] = dict_value.get("Ký hiệu")
        # item['ten_tienganh'] = dict_value.get("Tên tiếng Anh")
        # item['website'] = dict_value.get("Website")
        # item['tinh'] = dict_value.get("Tỉnh, thành phố")
        # item['loai_truong'] = dict_value.get("Loại trường")
        
        # yield item

        