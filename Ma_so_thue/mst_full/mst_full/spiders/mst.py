import scrapy
from scrapy import Request
from mst_full.items import MstFullItem
import pandas as pd

class MstSpider(scrapy.Spider):
    name = 'mst'
    allowed_domains = ['masothue.com']
    
    # def __init__(self, list_urls):
    #     self.list_urls = list_urls
        
    data_url = pd.read_csv('/Users/dinhvan/Projects/Code/web_scrape/scrapy/Ma_so_thue/ma_so_thu_Duoc/ma_so_thu_Duoc/spiders/9610.csv', dtype = str)
    start_urls = data_url['href'].to_list()
    # start_urls =['https://masothue.com/1500455159-010-cong-ty-trach-nhiem-huu-han-anh-dao-co-so-anh-dao-2']
    
    # custom_settings = {
    #     'FEEDS': {'/Users/dinhvan/Document/Projects/crawl_data/scrapy/mst_full/result_temp/result_temp.csv': {'format':'csv',}}
    # }
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url = url,callback=self.parse ,headers=headers)
            
    def parse(self, response):
        list_keys   = []
        list_values = []

        list_keys.extend((' Tên công ty',' URL'))

        list_values.append(response.xpath("//table[@class='table-taxinfo']/thead/tr/th/span[@class='copy']/text()").get())
        list_values.append(response.url)

        table1 = response.xpath("//table[@class='table-taxinfo']//tr/td[1]/text()").getall()
        table2 = response.xpath("//table[@class='table-taxinfo']//tr/td[2]/span[@class='copy']/text() | //table[@class='table-taxinfo']/tbody/tr/td/span/a/text() | //table[@class='table-taxinfo']//tr/td[2]/a/text() | //table[@class='table-taxinfo']//tr/td[2]/em/text()").getall()

        for i in table1:
            list_keys.append(i)
        del list_keys[-5:]

        for i in table2:
            list_values.append(i)
        
        list_keys.append(' Ngành nghề kinh doanh chính')
        list_values.append(response.xpath("//table[@class='table']//tr/td[2]/strong/a/text()").get())
        dict_result = dict(zip(list_keys,list_values))
    
        # print(dict_result)
        Item = MstFullItem()
        Item['url'] = dict_result.get(' URL')
        Item['ten_cong_ty'] = dict_result.get(' Tên công ty')
        Item['ten_quoc_te'] = dict_result.get(' Tên quốc tế')
        Item['ten_viet_tat'] = dict_result.get(' Tên viết tắt')
        Item['mst'] = dict_result.get(' Mã số thuế')
        Item['dia_chi'] = dict_result.get(' Địa chỉ')
        Item['dien_thoai'] = dict_result.get(' Điện thoại')
        Item['nghanh_nghe'] = dict_result.get(' Ngành nghề kinh doanh chính')
        Item['nguoi_dai_dien'] = dict_result.get(' Người đại diện')
        Item['ngay_hoat_dong'] = dict_result.get(' Ngày hoạt động')
        Item['quan_ly_boi'] = dict_result.get(' Quản lý bởi')
        Item['loai_hinh_DN'] = dict_result.get(' Loại hình DN')
        Item['tinh_trang'] = dict_result.get(' Tình trạng')
        yield Item
        # print(100000)
 