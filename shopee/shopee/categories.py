# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import (
#     ElementClickInterceptedException, 
#     TimeoutException, 
#     NoSuchElementException, 
#     TimeoutException, 
#     InvalidSessionIdException
#     )
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import time
# import pandas as pd
# import os

# options = Options()
# options.add_argument("--no-sandbox")
# options.add_argument("--headless")    
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-setuid-sandbox")
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

# def crawl():
#     dict_temp = dict.fromkeys(['pro_url','pro_name'])
    
    
#     browser = webdriver.Chrome(
#         service = Service(ChromeDriverManager().install()), 
#         chrome_options= options
#     )
#     browser.get(
#         "https://shopee.vn/all_categories"
#     )
#     WebDriverWait(browser, 20).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, "//div[@class='qYI3aj']/a[@class='Hs-Gh5'][1]")
#                 )
#             )
    
#     list_ele = browser.find_elements(By.XPATH,"//div[@class='qYI3aj']/a")
#     list_url = [elem.get_attribute('href') for elem in list_ele]
#     list_pro = [elem.text for elem in list_ele]
    
#     dict_temp['pro_url'] = list_url
#     dict_temp['pro_name'] = list_pro
    
#     time.sleep(5)
#     browser.close()
#     dataFrame = pd.DataFrame(dict_temp)
#     return dataFrame

# if __name__ == '__main__': 
#     crawl().to_csv('/Users/dinhvan/Projects/Code/web_scrape/scrapy/shopee/shopee/categories.csv', index = False


from shopee_crawler import Crawler

crawler = Crawler()
crawler.set_origin(origin="shopee.vn") # Input your root Shopee website of your country that you want to crawl

# data = crawler.crawl_by_shop_url(shop_url='https://shopee.vn/unistorevietnam?categoryId=100012&entryPoint=ShopByPDP&itemId=13759813343')

# data = crawler.crawl_by_cat_url(cat_url='https://shopee.vn/B%C3%A1ch-H%C3%B3a-Online-cat.11036525')

data = crawler.crawl_by_search(keyword='điện thoại samsung')

# data = crawler.crawl_cat_list()
print(data)