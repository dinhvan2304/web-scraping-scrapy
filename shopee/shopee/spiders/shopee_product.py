import scrapy


class ShopeeProductSpider(scrapy.Spider):
    name = 'shopee_product'
    allowed_domains = ['shopee.vn']
    start_urls = ['https://shopee.vn/Camera-Wifi-th%C3%B4ng-minh-EZVIZ-C6N-1080P-Camera-quay-qu%C3%A9t-wifi-d%C3%B9ng-cho-gia-%C4%91%C3%ACnh-digitalcamera-i.1082529536.23982068815?sp_atk=3d4ae2bd-63fb-44a1-a2d3-a93112a99ee8&xptdk=3d4ae2bd-63fb-44a1-a2d3-a93112a99ee8']

    def parse(self, response):
        test = response.xpath("//div[@class='flex-auto flex-column swTqJe']/div[@class='_44qnta']").extract_first()
        print(test)
        print('Ha Dinh Van')