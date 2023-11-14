import scrapy
import pandas as pd
from scrapy import Request
from CafeF.items import CafefItem

class CongtyconSpider(scrapy.Spider):
    name = 'congtycon'
    allowed_domains = ['cafef.vn'] 

    data_url = pd.read_csv('/Users/dinhvan/Documents/Projects/Crawl/selenium/SOE/url_HO_niem_yet.csv')
    # data_url.drop(data_url.loc[data_url['url'].isna()].index, inplace= True)
    # data_url['url'] = data_url['url'].loc(data_url['url'].isna() == False)
    start_urls = data_url['url'].values.tolist()
    # start_urls =['https://s.cafef.vn/Ajax/CongTy/CongTyCon.aspx?sym=BVH']
    def start_requests(self):
            for url in self.start_urls:
                yield Request(url,callback=self.parse)
                
    def parse(self, response):
        
        congtycon = response.xpath("//table//tr[2]/td/table[@class='congtycon']//tr/td[1]").getall()
        # congtylienket = response.xpath("//table//tr[4]/td/table[@class='congtycon']//tr/td[1]").getall()
        
        for i in range(2,len(congtycon)):
            ten_cty_con = response.xpath("//table//tr[2]/td/table[@class='congtycon']//tr[{}]/td[1]/text()".format(i)).extract_first()
            ten_cty_con = ten_cty_con.strip()
            if ten_cty_con == "":
                ten_cty_con = response.xpath("//table//tr[2]/td/table[@class='congtycon']//tr[{}]/td[1]/a/@title".format(i)).extract_first()
            
            ti_le = response.xpath("//table[@class='congtycon']//tr[{}]/td[4]/text()".format(i)).extract_first()
            dict_values = { 'mck_cong_ty_HO': response.url[-3:],
                            'ten_cong_ty_con': ten_cty_con,
                            'ti_le_so_huu' : ti_le
                }
            print(dict_values)
            
        # for i in range(2,len(congtylienket)):
        #     ten_cty_lien_ket = response.xpath("//table//tr[4]/td/table[@class='congtycon']//tr[{}]/td[1]/text()".format(i)).extract_first()
        #     ten_cty_lien_ket = ten_cty_lien_ket.strip()
        #     if ten_cty_lien_ket == "":
        #         ten_cty_lien_ket = response.xpath("//table//tr[4]/td/table[@class='congtycon']//tr[{}]/td[1]/a/@title".format(i)).extract_first()
                    
        #     dict_values = { 'mck_cong_ty_HO': response.url[-3:],
        #                     'ten_cong_ty_lien_ket': ten_cty_lien_ket,
        #                     'loai_hinh_doanh_nghiep' : 'Công ty liên kết'
        #         }
        #     print(dict_values)
                
                
            item = CafefItem()
            item['mck_cong_ty_HO'] = dict_values.get('mck_cong_ty_HO')
            item['ten_cong_ty_con'] = dict_values.get('ten_cong_ty_con')
            item['ti_le_so_huu'] = dict_values.get('ti_le_so_huu')
            yield item
    #    print(response.url)
