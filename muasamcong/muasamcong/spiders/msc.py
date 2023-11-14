import scrapy
import pandas as pd
from scrapy import Request
from muasamcong.items import MuasamcongItem

class MscSpider(scrapy.Spider):
    name = 'msc'
    allowed_domains = ['muasamcong.mpi.gov.vn']
    data_url = pd.read_csv('/Users/dinhvan/Documents/Projects/Crawl/jupyter/muasamcong/url_muasamcong.csv')
    start_urls = data_url['url'].to_list()
    # start_urls =['http://muasamcong.mpi.gov.vn:8081/biddauthau/trangchu/tbmt/viewChiTiet?bidNo=20220940766&bidTurnNo=00&lang=']
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)

    def parse(self, response):
        url = response.url
        key = response.xpath("//table[@class='tr']//tr/td[@class='tdlabel']/text()").getall()
        subtitle = response.xpath("//table[@class='tr']//tr[7]/td[@class='subtitle']/text()").get()
        
        if 'Thời điểm\r\n\t\t\t\t\t\t\t\t\t\tđăng tải\xa0' in key:
            t1 = key.index('Thời điểm\r\n\t\t\t\t\t\t\t\t\t\tđăng tải\xa0')
            if subtitle is None:
                t1 = t1 + 10
            else :
                t1 = t1 + 13
            thoi_dien_dang_tai = response.xpath("//table[@class='tr']//tr[{}]/td[@class='tdcontrol'][2]/text()".format(t1)).extract_first()
        else :
            thoi_dien_dang_tai = 1
            
        if '\xa0Thời gian nhận E-HSDT từ ngày' in key :
            t2 = key.index('\xa0Thời gian nhận E-HSDT từ ngày') 
            if subtitle is None:
                t2 = t2+ 15
            else :
                t2 = t2 + 18
            
            thoi_diem_nhan_EHSDT = response.xpath("//table[@class='tr']//tr[1]/td/table[@class='tr']//tr[{}]/td[@class='tdcontrol'][1]/text()".format(t2)).extract_first()
            den_ngay = response.xpath("//table[@class='tr']//tr[1]/td/table[@class='tr']//tr[{}]/td[@class='tdcontrol'][2]/text()".format(t2)).extract_first()
            t3 = key.index('\xa0Thời điểm đóng/mở thầu') 
            
            if subtitle is None:
                t3 = t3 + 18
            else :
                t3 = t3 + 21
            thoi_diem_dong_mo = response.xpath("//table[@class='tr']//tr[1]/td/table[@class='tr']//tr[{}]/td[@class='tdcontrol']/text()".format(t3)).extract_first()
            
        elif '\xa0 \r\n\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\tThời gian bán HSYC từ\r\n\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t' in key :
            t2 = key.index('\xa0 \r\n\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\tThời gian bán HSYC từ\r\n\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t') 
            if subtitle is None:
                t2 = t2+ 10
            else :
                t2 = t2 + 13
            
            thoi_diem_nhan_EHSDT = response.xpath("//table[@class='tr']//tr[1]/td/table[@class='tr']//tr[{}]/td[@class='tdcontrol'][1]/text()".format(t2)).extract_first()
            den_ngay = response.xpath("//table[@class='tr']//tr[1]/td/table[@class='tr']//tr[{}]/td[@class='tdcontrol'][2]/text()".format(t2)).extract_first()
            
            t3 = key.index('\xa0Thời điểm mở\r\n\t\t\t\t\t\t\t\t\t\tthầu') 
            if subtitle is None:
                t3 = t3 + 9
            else :
                t3 = t3 + 12
            thoi_diem_dong_mo = response.xpath("//table[@class='tr']//tr[1]/td/table[@class='tr']//tr[{}]/td[@class='tdcontrol']/text()".format(t3)).extract_first()
        
        elif '\xa0 \r\n\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\tThời gian bán HSMT từ\r\n\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t' in key :
            t2 = key.index('\xa0 \r\n\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\tThời gian bán HSMT từ\r\n\t\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t\t\r\n\t\t\t\t\t\t\t\t\t') 
            if subtitle is None:
                t2 = t2+ 10
            else :
                t2 = t2 + 13
            
            thoi_diem_nhan_EHSDT = response.xpath("//table[@class='tr']//tr[1]/td/table[@class='tr']//tr[{}]/td[@class='tdcontrol'][1]/text()".format(t2)).extract_first()
            den_ngay = response.xpath("//table[@class='tr']//tr[1]/td/table[@class='tr']//tr[{}]/td[@class='tdcontrol'][2]/text()".format(t2)).extract_first()
            
            t3 = key.index('\xa0Thời điểm mở\r\n\t\t\t\t\t\t\t\t\t\tthầu') 
            if subtitle is None:
                t3 = t3 + 9
            else :
                t3 = t3 + 12
            thoi_diem_dong_mo = response.xpath("//table[@class='tr']//tr[1]/td/table[@class='tr']//tr[{}]/td[@class='tdcontrol']/text()".format(t3)).extract_first()
        
        else:
            thoi_diem_dong_mo = 1
            den_ngay = 1
            thoi_diem_nhan_EHSDT = 1
        
            
            
        # print(t1)
        # print(t2)
        # print(t3)
            
            
            
        # print(key)
   
        item = MuasamcongItem()
        item['url'] = url
        item['thoi_diem_dang_tai'] = thoi_dien_dang_tai
        item['thoi_diem_nhan_EHSDT']   = thoi_diem_nhan_EHSDT
        item['thoi_diem_dong_mo']      = thoi_diem_dong_mo
        item['den_ngay'] = den_ngay
        
        yield item
