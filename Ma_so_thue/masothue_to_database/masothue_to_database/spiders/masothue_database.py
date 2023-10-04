import scrapy
from scrapy.http import Request
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote
from masothue_to_database.items import MasothueToDatabaseItem

TYPE_UPDATE = 0
TYPE_INSERT = 1

class MasothueDatabaseSpider(scrapy.Spider):
    name = 'masothue_database'
    allowed_domains = ['masothue.com']
    start_urls = ['http://masothue.com/']
    custom_settings={
        "ITEM_PIPELINES": {
            "masothue_to_database.pipelines.MasothueToDatabasePipeline": 300,
        },
        "ITEM_CLASS": "masothue_to_database.items.MasothueToDatabaseItem",
    }
    def start_requests(self):
        mst_urls = pd.read_csv('/Users/dinhvan/Document/Projects/crawl_data/scrapy/masothue_to_database/masothue_url.csv', dtype = str)
        mst_urls["mst_check"] = "'" + mst_urls["mst"]
        
        append_type = TYPE_INSERT
        if append_type == TYPE_INSERT:
            sqlEngine = create_engine("mysql+pymysql://vantt:%s@172.16.10.144:3306/hkd" % quote("Ptdl@123"))
            query_origin = "SELECT DISTINCT mst as mst_check FROM clients"
            mst_existed = pd.read_sql(query_origin, con = sqlEngine)
            print(mst_existed)
            df_all = mst_urls.merge(
                mst_existed.drop_duplicates(),
                on=["mst_check"],
                how="left",
                indicator=True,
            )
            ma_so_thue_urls = df_all[df_all["_merge"] == "left_only"]['url'].values.tolist()
        elif append_type == TYPE_UPDATE:
            ma_so_thue_urls = mst_urls['url'].values.tolist()

        requests = [Request(url = url, callback=self.parse,
                    dont_filter=True, meta={
                        'append_type': append_type
                    }) for url in ma_so_thue_urls]
        if len(requests) > 0:
            return requests
        else:
            pass
        # request = [Request(url="https://masothue.com/0317336369-cong-ty-tnhh-cong-nghiep-xuat-nhap-khau-duc-tien", callback=self.parse,
        #             dont_filter=True)]
        # return request 
    
    def parse_city(self, response):
        cities = response.xpath("//ul[@class='row']/li[@class='cat-item col-xs-6 col-md-12']/a/@href").extract()
        for city in cities:
            city_url = response.urljoin(city)
            yield scrapy.Request(
                city_url,
                callback=self.parse_street,
                dont_filter=True
            )

    def parse_street(self, response):
        streets = response.xpath("//ul[@class='row']/li[@class='cat-item col-xs-6 col-md-12']/a/@href").extract()
        for street in streets:
            street_url = response.urljoin(street)
            yield scrapy.Request(
                street_url,
                callback=self.parse_town,
                dont_filter=True
            )   
    
    def parse_town(self, response):
        towns = response.xpath("//ul[@class='row']/li[@class='cat-item col-xs-6 col-md-12']/a/@href").extract()
        for town in towns:
            town_url = response.urljoin(town)
            yield scrapy.Request(
                town_url,
                callback=self.parse_page,
                dont_filter=True,
                meta={
                    'town_url': town_url
                    }
            )

    def parse_page(self, response):
        city = response.xpath("//div[@class='container']/nav[@class='woocommerce-breadcrumb']/span[5]/a/span/text()").get()
        street = response.xpath("//div[@class='container']/nav[@class='woocommerce-breadcrumb']/span[7]/a/span/text()").get()
        town_url = response.meta.get('town_url')
        for index_page in range(1, 11):
            page_url = town_url + '?page=' + str(index_page)
            yield scrapy.Request(
                page_url,
                callback=self.parse_info,
                dont_filter=True,
                meta={
                    'city': city,
                    'street': street,
                    'town_url': town_url
                    }
            )
    
    def convert_new_phone(self, number):
        new_digits_phone = {
            "0169": "039",
            "0168": "038",
            "0167": "037",
            "0166": "036",
            "0165": "035",
            "0164": "034",
            "0163": "033",
            "0162": "032",
            "0128": "088",
            "0123": "083",
            "0124": "084",
            "0125": "085",
            "0127": "081",
            "0129": "082",
            "0120": "070",
            "0121": "079",
            "0122": "077",
            "0126": "076",
            "0128": "078",
            "0182": "052",
            "0186": "056",
            "0188": "058",
            "0199": "059",
        }
        result = number
        start_phone_digits = result[:4]
        if start_phone_digits in new_digits_phone.keys():
            new_digits = new_digits_phone[start_phone_digits]
        else:
            new_digits = None
        if new_digits != None:
            result = new_digits + result[4:]
        
        return result

    def parse_info(self, response):
        city = response.meta.get('city')
        street = response.meta.get('street')
        company_url = response.xpath("//div[@class='container']/div[@class='tax-listing']/div/h3/a/@href").extract()
        for url in company_url:
            company_info_url = response.urljoin(url)
            yield scrapy.Request(
                company_info_url,
                callback=self.parse,
                dont_filter=True,
                meta={
                    'city': city,
                    'street': street
                    }
            )
            
    def matchingKeys(self, dictionary, searchString):
        return [
            key for key, val in dictionary.items() if any(searchString in s for s in val)
        ]

    def parse(self, response):
        append_type = response.meta.get('append_type')
        
        all_info = []
        Ma_TTP = {
            "HNI": "TTKD Hà Nội",
            "VPC": "TTKD Vĩnh Phúc",
            "HBH": "TTKD Hòa Bình",
            "BNH": "TTKD Bắc Ninh",
            "BCN": "TTKD Bắc Kạn",
            "LCI": "TTKD Lào Cai",
            "LSN": "TTKD Lạng Sơn",
            "BGG": "TTKD Bắc Giang",
            "CBG": "TTKD Cao Bằng",
            "TNN": "TTKD Thái Nguyên",
            "PTO": "TTKD Phú Thọ",
            "TQG": "TTKD Tuyên Quang",
            "YBI": "TTKD Yên Bái",
            "SLA": "TTKD Sơn La",
            "DBN": "TTKD Điện Biên",
            "LCU": "TTKD Lai Châu",
            "HGG": "TTKD Hà Giang",
            "HNM": "TTKD Hà Nam",
            "NDH": "TTKD Nam Định",
            "TBH": "TTKD Thái Bình",
            "HDG": "TTKD Hải Dương",
            "HPG": "TTKD Hải Phòng",
            "QNH": "TTKD Quảng Ninh",
            "HYN": "TTKD Hưng Yên",
            "NBH": "TTKD Ninh Bình",
            "THA": "TTKD Thanh Hoá",
            "NAN": "TTKD Nghệ An",
            "HTH": "TTKD Hà Tĩnh",
            "QBH": "TTKD Quảng Bình",
            "QTI": "TTKD Quảng Trị",
            "HUE": "TTKD Thừa Thiên-Huế",
            "QNM": "TTKD Quảng Nam",
            "QNI": "TTKD Quảng Ngãi",
            "BDH": "TTKD Bình Định",
            "GLI": "TTKD Gia Lai",
            "DLC": "TTKD Đắk Lắk",
            "DKN": "TTKD Đắk Nông",
            "PYN": "TTKD Phú Yên",
            "KHA": "TTKD Khánh Hòa",
            "KTM": "TTKD KonTum",
            "DNG": "TTKD Đà Nẵng",
            "LDG": "TTKD Lâm Đồng",
            "BTN": "TTKD Bình Thuận",
            "NTN": "TTKD Ninh Thuận",
            "HCM": "TTKD TP Hồ Chí Minh",
            "DNI": "TTKD Đồng Nai",
            "BDG": "TTKD Bình Dương",
            "TNH": "TTKD Tây Ninh",
            "VTU": "TTKD Bà Rịa- Vũng Tàu",
            "BPC": "TTKD Bình Phước",
            "LAN": "TTKD Long An",
            "TGG": "TTKD Tiền Giang",
            "BTE": "TTKD Bến Tre",
            "TVH": "TTKD Trà Vinh",
            "VLG": "TTKD Vĩnh Long",
            "CTO": "TTKD Cần Thơ",
            "HAG": "TTKD Hậu Giang",
            "DTP": "TTKD Đồng Tháp",
            "AGG": "TTKD An Giang",
            "KGG": "TTKD Kiên Giang",
            "CMU": "TTKD Cà Mau",
            "STG": "TTKD Sóc Trăng",
            "BLU": "TTKD Bạc Liêu",
        }

        Vung_TTP = {
            "MB": "Lào Cai,  Điện Biên, Hòa Bình, Lai Châu, Sơn La, Hà Giang, Cao Bằng, Bắc Kạn, Lạng Sơn, Tuyên Quang, Thái Nguyên, Phú Thọ, Bắc Giang, Quảng Ninh, Bắc Ninh, Hà Nam, Hà Nội, Hải Dương, Thanh Hoá, Hưng Yên,  Nam Định, Thái Bình, Vĩnh Phúc",
            "MT": "Yên Bái, Nghệ An, Ninh Bình, Tuyên Quang, Hà Tĩnh , Quảng Bình,  Quảng Trị, Thừa Thiên-Huế, Đà Nẵng, Quảng Nam, Quảng Ngãi, Bình Định, Phú Yên, Khánh Hòa, KonTum, Gia Lai, Đắk Lắk, Đắk Nông, Hải Phòng",
            "MN": "Bình Phước, Ninh Thuận, Bình Thuận, Bình Dương, Đồng Nai, Tây Ninh, Bà Rịa-Vũng Tàu, Thành phố Hồ Chí Minh, Long An, Đồng Tháp, Tiền Giang, An Giang, Bến Tre, Vĩnh Long, Trà Vinh, Hậu Giang, Kiên Giang, Sóc Trăng, Bạc Liêu, Cà Mau, Thành phố Cần Thơ, Lâm Đồng",
        }

        Phone_Prefix_Vina = {
            "8496": "Viettel",
            "8497": "Viettel",
            "8498": "Viettel",
            "8432": "Viettel",
            "8433": "Viettel",
            "8434": "Viettel",
            "8435": "Viettel",
            "8436": "Viettel",
            "8437": "Viettel",
            "8438": "Viettel",
            "8439": "Viettel",
            "8486": "Viettel",
            "8490": "Mobifone",
            "8493": "Mobifone",
            "8470": "Mobifone",
            "8489": "Mobifone",
            "8477": "Mobifone",
            "8476": "Mobifone",
            "8478": "Mobifone",
            "8479": "Mobifone",
            "8491": "Vinaphone",
            "8494": "Vinaphone",
            "8481": "Vinaphone",
            "8482": "Vinaphone",
            "8483": "Vinaphone",
            "8484": "Vinaphone",
            "8485": "Vinaphone",
            "8488": "Vinaphone",
            "8499": "Gmobile",
            "8459": "Gmobile",
            "8492": "Vietnamobile",
            "8456": "Vietnamobile",
            "8458": "Vietnamobile",
            "": "khác"
        }
        code_nganh_chinh = {
            "A": [str(i).zfill(2) for i in range(1, 4)],
            "B": [str(i).zfill(2) for i in range(5, 10)],
            "C": [str(i).zfill(2) for i in range(10, 34)],
            "D": [str(35).zfill(2)],
            "E": [str(i).zfill(2) for i in range(36, 40)],
            "F": [str(i).zfill(2) for i in range(41, 44)],
            "G": [str(i).zfill(2) for i in range(45, 48)],
            "H": [str(i).zfill(2) for i in range(49, 54)],
            "I": [str(i).zfill(2) for i in range(55, 57)],
            "J": [str(i).zfill(2) for i in range(58, 64)],
            "K": [str(i).zfill(2) for i in range(64, 67)],
            "L": [str(68).zfill(2)],
            "M": [str(i).zfill(2) for i in range(69, 76)],
            "N": [str(i).zfill(2) for i in range(77, 83)],
            "O": [str(84).zfill(2)],
            "P": [str(85).zfill(2)],
            "Q": [str(i).zfill(2) for i in range(86, 89)],
            "R": [str(i).zfill(2) for i in range(90, 94)],
            "S": [str(i).zfill(2) for i in range(94, 97)],
            "T": [str(i).zfill(2) for i in range(97, 99)],
            "U": [str(99).zfill(2)],
        }
        # city = response.meta.get('city')
        # street = response.meta.get('street')
        title = response.xpath("//div[@class='container']/header/h1[@class='h1']/text()").extract_first()
        vi_name = response.xpath("//table[@class='table-taxinfo']/thead/tr/th/span[@class='copy']/text()").get()
        companies_info_title = response.xpath("//table[@class='table-taxinfo']//tr/td[1]/text()").extract()
        companies_info_detail = response.xpath("//table[@class='table-taxinfo']//tr/td[2]")
        # businesses_code = response.xpath("//table[@class='table']//tr[@class='p045rem']/td[1]")
        # businesses = response.xpath("//table[@class='table']/tbody/tr[@class='p045rem']/td[2]")
        businesses_code = response.xpath("//div[@class='container']/table[@class='table']//tr/td[1]")
        businesses = response.xpath("//div[@class='container']/table[@class='table']//tr/td[2]")

        item_info = []
        companies_info_detail_parse = []
        business_parse = []

        if len(companies_info_detail) > 0:
            for cid in companies_info_detail:
                if cid.xpath(".//span/text()").extract_first() is None:
                    if cid.xpath('.//a/text()').extract_first() is None:
                        temp_cid = ''
                    else:
                        temp_cid = ''.join(cid.xpath('.//a/text()').extract_first())
                else:
                    temp_cid = ''.join(cid.xpath(".//span/text()").extract_first())
                
                companies_info_detail_parse.append(temp_cid)

            company_info = {}
            for idx, val in enumerate(companies_info_detail_parse):
                company_info[companies_info_title[idx].strip().replace('\n', '')] = val
            
            en_name = ""
            if en_name in company_info.keys():
                en_name = company_info["Tên quốc tế"]
                
            if "Mã số thuế" in company_info.keys():
                mst = "'" + company_info["Mã số thuế"]
            elif "Mã số thuế cá nhân" in company_info.keys():
                mst = "'" + company_info["Mã số thuế cá nhân"]
            else:
                mst = ""
            
            if "Điện thoại" in company_info.keys(): 
                phone = company_info["Điện thoại"]
                phone = self.convert_new_phone(phone)
                if phone.startswith("0"):
                    phone = "84" + phone[1:]

                prefix_phone = phone[:4]
            else:
                phone = ""
                prefix_phone = ""
            telco_name = "khác"
            try:
                telco_name = Phone_Prefix_Vina.get(prefix_phone)
            except KeyError as e:
                print(e)
                pass

            enterprise_type = "khác"
            # enterprise_type = company_info["Loại hình pháp lý"]
            if "Loại hình DN" in company_info.keys():
                enterprise_type = company_info["Loại hình DN"]
            else:
                if "tnhh" in title.lower():
                    enterprise_type = "TNHH"
                elif "cổ phần" in title.lower() or "cp" in title.lower():
                    enterprise_type = "CTCP"

            if "Người đại diện" in company_info.keys():
                manager_name = company_info["Người đại diện"]
            else:
                manager_name = ""

            if "Ngày hoạt động" in company_info.keys():
                created_date = company_info["Ngày hoạt động"]
            else:
                created_date = ""

            dia_chi = company_info["Địa chỉ"]
            dia_chi_list = dia_chi.split(",")
            if len(dia_chi_list) > 3:
                # city = dia_chi_list[-1]
                # street = dia_chi_list[-2]
                # district = dia_chi_list[-3]
                city = dia_chi_list[-2].strip()
                street = dia_chi_list[-3].strip()
                district = dia_chi_list[-4].strip()
                location = " ".join(dia_chi_list[:-3])
            else:
                city = ""
                street = ""
                district = ""
                location = dia_chi

            split_city = city.split(" ")
            if len(split_city) > 0:
                city_check = " ".join(split_city[-2:])

                province_code = [key for key in Ma_TTP if city_check in Ma_TTP[key]]
                if len(province_code) > 0:
                    province_code = province_code[0]
                else:
                    province_code = "..."

                province_zip = [key for key in Vung_TTP if city_check in Vung_TTP[key]]
                if len(province_zip) > 0:
                    province_zip = province_zip[0]
                else:
                    province_zip = "..."
            else:
                province_code = "..." 
                province_zip = "..."

            status = ""
            if "Tình trạng" in company_info.keys(): 
                status = company_info["Tình trạng"]

            business_list = []
            main_business = ""
            main_business_code = ""
            for index, bus in enumerate(businesses):
                # if bus.xpath(".//strong/a/text()").get() is None:
                #     business = bus.xpath(".//a/text()").get()
                #     business_code = businesses_code[index].xpath(".//a/text()").get()
                # else:
                #     business = bus.xpath(".//strong/a/text()").get()
                #     main_business = business
                #     business_code = businesses_code[index].xpath(".//strong/a/text()").get()
                #     # main_business_code = business_code[0]
                if bus.xpath(".//strong").get() is None:
                    business = bus.xpath(".//a/text()").get()
                    business_code = businesses_code[index].xpath(".//a/text()").get()
                else:
                    business = bus.xpath(".//strong/text()").get()
                    if not business:
                        business = bus.xpath(".//strong/a/text()").get() 
                    business_code = businesses_code[index].xpath(".//strong/a/text()").get()
                    temp_business_code = self.matchingKeys(code_nganh_chinh, business_code[:2])
                    if len(temp_business_code) > 0:
                        main_business_code = temp_business_code[0]
                    main_business = business + " " +  business_code
                business_list.append("{}. {} {}".format(index+1, business, business_code))
            
            bussiness_detail = "\n".join(business_list)

            print(vi_name)
            
            mst_info = MasothueToDatabaseItem()
            mst_info["province"] = province_zip
            mst_info["province_code"] = province_code
            mst_info["vi_name"] = vi_name
            mst_info["en_name"] = en_name
            mst_info["mst"] = mst
            mst_info['city'] = city
            mst_info["street"] = street
            mst_info["district"] = district
            mst_info["location"] = location
            mst_info["phone"] = phone
            mst_info["telco"] = telco_name
            mst_info["manager_name"] = manager_name
            mst_info["created_date"] = created_date
            mst_info["main_business"] = main_business
            mst_info["main_business_code"] = main_business_code
            mst_info["enterprise_type"] = enterprise_type
            mst_info["status"] = status
            mst_info['business'] = bussiness_detail
            mst_info['append_type'] = append_type

            yield mst_info
        else:
            pass
        

