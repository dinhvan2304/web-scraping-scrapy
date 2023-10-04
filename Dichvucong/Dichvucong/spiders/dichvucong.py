import scrapy
from scrapy import Request
import pandas as pd
import os
from Dichvucong.items import DichvucongItem
class DichvucongSpider(scrapy.Spider):
    name = 'dichvucong'
    allowed_domains = ['dmec.moh.gov.vn']
    urls = []
    for page in range(1,922,1):
        urls.append("https://dmec.moh.gov.vn/van-ban-cong-bo?p_p_id=vanbancongbo_WAR_trangthietbiyteportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_vanbancongbo_WAR_trangthietbiyteportlet_keyword=&_vanbancongbo_WAR_trangthietbiyteportlet_showHide=1&_vanbancongbo_WAR_trangthietbiyteportlet_ngayGuiTu=&_vanbancongbo_WAR_trangthietbiyteportlet_ngayGuiDen=&_vanbancongbo_WAR_trangthietbiyteportlet_ngayCongBoTu=&_vanbancongbo_WAR_trangthietbiyteportlet_ngayCongBoDen=&_vanbancongbo_WAR_trangthietbiyteportlet_tenDoanhNghiep=&_vanbancongbo_WAR_trangthietbiyteportlet_tenTTBYT=&_vanbancongbo_WAR_trangthietbiyteportlet_coQuanQuanLyId=0&_vanbancongbo_WAR_trangthietbiyteportlet_tthcId=0&_vanbancongbo_WAR_trangthietbiyteportlet_delta=75&_vanbancongbo_WAR_trangthietbiyteportlet_keywords=&_vanbancongbo_WAR_trangthietbiyteportlet_advancedSearch=false&_vanbancongbo_WAR_trangthietbiyteportlet_andOperator=true&_vanbancongbo_WAR_trangthietbiyteportlet_resetCur=false&_vanbancongbo_WAR_trangthietbiyteportlet_cur={}".format(page))

    start_urls = urls
    # start_urls = ['https://dmec.moh.gov.vn/van-ban-cong-bo?p_p_id=vanbancongbo_WAR_trangthietbiyteportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_vanbancongbo_WAR_trangthietbiyteportlet_keyword=&_vanbancongbo_WAR_trangthietbiyteportlet_showHide=1&_vanbancongbo_WAR_trangthietbiyteportlet_ngayGuiTu=&_vanbancongbo_WAR_trangthietbiyteportlet_ngayGuiDen=&_vanbancongbo_WAR_trangthietbiyteportlet_ngayCongBoTu=&_vanbancongbo_WAR_trangthietbiyteportlet_ngayCongBoDen=&_vanbancongbo_WAR_trangthietbiyteportlet_tenDoanhNghiep=&_vanbancongbo_WAR_trangthietbiyteportlet_tenTTBYT=&_vanbancongbo_WAR_trangthietbiyteportlet_coQuanQuanLyId=0&_vanbancongbo_WAR_trangthietbiyteportlet_tthcId=0&_vanbancongbo_WAR_trangthietbiyteportlet_delta=75&_vanbancongbo_WAR_trangthietbiyteportlet_keywords=&_vanbancongbo_WAR_trangthietbiyteportlet_advancedSearch=false&_vanbancongbo_WAR_trangthietbiyteportlet_andOperator=true&_vanbancongbo_WAR_trangthietbiyteportlet_resetCur=false&_vanbancongbo_WAR_trangthietbiyteportlet_cur=200']
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
            
    def parse(self, response):
        for value in range(2,77,1):
            dict_temp = {
                "stt" : response.xpath("//table[@class='oep-table']//tr[{}]/td[1]/text()".format(value)).get(),
                "ma_ho_so" : response.xpath("//table[@class='oep-table']//tr[{}]/td[2]/text()".format(value)).get(),
                "thong_tin" : response.xpath("//table[@class='oep-table']//tr[{}]/td[4]/label/a/text()".format(value)).get(),
                "href": response.xpath("//table[@class='oep-table']//tr[{}]/td[4]/label/a/@href".format(value)).get(),
                "so_cong_bo" : response.xpath("//table[@class='oep-table']//tr[{}]/td[3]/text()".format(value)).get(),
                "ten_doanh_nghiep" : response.xpath("//table[@class='oep-table']//tr[{}]/td[5]/text()".format(value)).get(),
                "ten_TTBYT" : response.xpath("//table[@class='oep-table']//tr[{}]/td[6]/span/text()".format(value)).get(),
                "trang_thai" : response.xpath("//table[@class='oep-table']//tr[{}]/td[7]/p/text()".format(value)).get()
            }
            
            # if all(value == None for value in dict_temp.values()) ==  False:
            # result = DichvucongItem()
            # result['stt'] = dict_temp['stt']
            # result['ma_ho_so'] = dict_temp['ma_ho_so']
            # result['thong_tin'] = dict_temp['thong_tin']
            # result['href'] = dict_temp['href']
            # result['so_cong_bo'] = dict_temp['so_cong_bo']
            # result['ten_doanh_nghiep'] = dict_temp['ten_doanh_nghiep']
            # result['ten_TTBYT'] = dict_temp['ten_TTBYT']
            # result['trang_thai'] = dict_temp['trang_thai']
            # yield result
            # # break
            data = pd.DataFrame([dict_temp])
            resutl_path = '/Users/dinhvan/Projects/Code/web_scrape/scrapy/Dichvucong/Dichvucong/spiders/info_temp.csv'
            # data.to_csv(resutl_path, index= False)
            # break
            data.to_csv(resutl_path, mode='a', header=not os.path.exists(resutl_path), index = False)
    
    
    