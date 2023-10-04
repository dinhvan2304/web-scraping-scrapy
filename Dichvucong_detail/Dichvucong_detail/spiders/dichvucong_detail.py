import scrapy
import pandas as pd
from scrapy import Request
import os


class DichvucongDetailSpider(scrapy.Spider):
    name = 'dichvucong_detail'
    allowed_domains = ['dmec.moh.gov.vn']
    href = pd.read_csv('/Users/dinhvan/Projects/Code/web_scrape/scrapy/Dichvucong/Dichvucong/spiders/info_temp.csv',dtype= str)
    href = href.loc[href['thong_tin'] == 'Công bố tiêu chuẩn áp dụng đối với trang thiết bị y tế loại B']
    start_urls = href['href'].to_list()
    # start_urls = ['https://dmec.moh.gov.vn/van-ban-cong-bo?p_p_id=vanbancongbo_WAR_trangthietbiyteportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_vanbancongbo_WAR_trangthietbiyteportlet_hoSoId=340502&_vanbancongbo_WAR_trangthietbiyteportlet_vanBanId=237411&_vanbancongbo_WAR_trangthietbiyteportlet_doanhNghiepId=2316&_vanbancongbo_WAR_trangthietbiyteportlet_redirectVanBanURL=%2Fvan-ban-cong-bo%3Fp_p_id%3Dvanbancongbo_WAR_trangthietbiyteportlet%26p_p_lifecycle%3D0%26p_p_state%3Dnormal%26p_p_mode%3Dview%26p_p_col_id%3Dcolumn-1%26p_p_col_count%3D1%26_vanbancongbo_WAR_trangthietbiyteportlet_jspPage%3D%252Fhtml%252Fttbyte%252Fportlet%252Fvanbancongbo%252Fview.jsp&_vanbancongbo_WAR_trangthietbiyteportlet_jspPage=%2Fhtml%2Fttbyte%2Fportlet%2Fvanbancongbo%2Fxemhoso_tuybien.jsp']
    
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        for url in self.start_urls:
            yield Request(url,callback=self.parse ,headers=headers)
    def parse(self, response):
        columns = ["company_name","product_owner","company_address","phone_number","fax","type","email","representative","landline_number","mst","product"]

        company_name = response.xpath("//form[@id='_vanbancongbo_WAR_trangthietbiyteportlet_fm']/div[@id='oep-hoso-content']/div[@class='maudon']/div[4]/p[1]/span[@class='text_value']/text()").extract_first()
        mst = response.xpath("//form[@id='_vanbancongbo_WAR_trangthietbiyteportlet_fm']/div[@id='oep-hoso-content']/div[@class='maudon']/div[4]/div[1]/p[1]/span[@class='text_value']/text()").extract_first()
        # product_owner = response.xpath("//form[@id='_vanbancongbo_WAR_trangthietbiyteportlet_fm']/div[@id='oep-hoso-content']/div[@class='maudon']/div[4]/div[1]/p[2]/span[@class='text_value']/text()").extract_first()
        
        company_address = (response.xpath("//form[@id='_vanbancongbo_WAR_trangthietbiyteportlet_fm']/div[@id='oep-hoso-content']/div[@class='maudon']/div[4]/div[1]/p[2]/span[@class='text_value']/text()").extract_first()).replace('\n','').replace('\t','')
        
        phone_number = response.xpath("//form[@id='_vanbancongbo_WAR_trangthietbiyteportlet_fm']/div[@id='oep-hoso-content']/div[@class='maudon']/div[4]/div[1]/p[3]/span[@class='text_value'][1]/text()").extract_first()
        
        email = response.xpath("//form[@id='_vanbancongbo_WAR_trangthietbiyteportlet_fm']/div[@id='oep-hoso-content']/div[@class='maudon']/div[4]/div[1]/p[4]/span[@class='text_value']/text()").extract_first()
        
        # fax = response.xpath("//form[@id='_vanbancongbo_WAR_trangthietbiyteportlet_fm']/div[@id='oep-hoso-content']/div[@class='maudon']/div[4]/div[1]/p[3]/span[@class='text_value'][2]/text()").extract_first()
 
        representative = response.xpath("//form[@id='_vanbancongbo_WAR_trangthietbiyteportlet_fm']/div[@id='oep-hoso-content']/div[@class='maudon']/div[4]/div[2]/p[1]/span[@class='text_value']/text()").extract_first()
        
        landline_number = response.xpath("//form[@id='_vanbancongbo_WAR_trangthietbiyteportlet_fm']/div[@id='oep-hoso-content']/div[@class='maudon']/div[4]/div[2]/p[3]/span[@class='text_value'][1]/text()").extract_first()

        product = response.xpath("//form[@id='_vanbancongbo_WAR_trangthietbiyteportlet_fm']/div[@id='oep-hoso-content']/div[@class='maudon']/div[4]/div[3]/p[1]/span[@class='text_value']/text()").extract_first()
        dict_temp = {
            "company_name":company_name,
            "mst":mst,
            # "product_owner": product_owner,
            "company_address":company_address,
            # "phone_number":phone_number,
            "email":email,
            "representative":representative,
            "landline_number":landline_number,
            # "fax":fax,
            "product" : product,
            "type":"Công bố tiêu chuẩn áp dụng đối với trang thiết bị y tế loại B"
        }
        data = pd.DataFrame([dict_temp])
        data = data.reindex(columns=columns)
        # print(dict_temp)
        # data.to_csv('/Users/dinhvan/Projects/Code/web_scrape/scrapy/Dichvucong_detail/Dichvucong_detail/kqdvc.csv', index= False)
        resutl_path = '/Users/dinhvan/Projects/Code/web_scrape/scrapy/Dichvucong_detail/Dichvucong_detail/kqdvc.csv'
        data.to_csv(resutl_path, mode='a', header=not os.path.exists(resutl_path), index = False)