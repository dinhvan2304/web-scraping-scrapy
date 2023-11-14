# from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementClickInterceptedException, 
    TimeoutException, 
    NoSuchElementException, 
    TimeoutException, 
    InvalidSessionIdException
    )
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import pandas as pd
import os
from seleniumwire import webdriver

options = Options()
options.add_argument("--no-sandbox")
# options.add_argument("--headless")    
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

def crawl():
    dict_temp = dict.fromkeys(['pro_url','pro_name'])
    
    
    browser = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )
    browser.get(
        "https://shopee.vn/D%C3%A9p-cross-Sandal-D%C3%A9p-%C4%90%E1%BA%BF-D%C3%A0y-Si%C3%AAu-Nh%E1%BA%B9-t%E1%BA%B7ng-k%C3%A8m-b%E1%BB%99-h%C3%ACnh-g%E1%BA%AFn-Kaws-v%C3%A0-ch%C3%B3-si%C3%AAu-xinh-T%E1%BA%B7ng-h%C3%ACnh-g%E1%BA%AFn-nh%C6%B0-%E1%BA%A3nh--i.637051265.20164003135?sp_atk=7e07d1eb-fc17-40ec-a321-ede72af7be5c&xptdk=7e07d1eb-fc17-40ec-a321-ede72af7be5c"
    )
    # time.sleep(10)
    # test = browser.find_element(By.XPATH,"//div[@class='flex-auto flex-column swTqJe']/div[@class='_44qnta']/span").text
    text = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='col-xs-2-4 shopee-search-item-result__item'][1]/a/div[@class='gHKRq2']/div[@class='eAPUFG']/div[@class='J1Dw2W']/div[@class='OspxFR']/div[@class='v5rrDh']/div[@class='APSFjk cB928k skSW9t']")
                )
            ).text
    time.sleep(10)
    # browser.find_element(By.XPATH,"//div[@class='shopee-filter-group shopee-facet-filter']/div[@class='folding-items shopeee-filter-group__body folding-items--folded']/div[@class='stardust-dropdown folding-items__toggle']/div[@class='stardust-dropdown__item-header']/div[@class='shopee-filter-group__toggle-btn']").click()
    
    
    # category_num = len(browser.find_elements(By.XPATH,"//div[@class='shopee-filter-panel']/div[@class='shopee-filter-group shopee-facet-filter']/div[@class='folding-items shopeee-filter-group__body folding-items--folded']//div[@class='shopee-checkbox']/label[@class='shopee-checkbox__control']/span[@class='shopee-checkbox__label']"))
    

    browser.close()
    return text

if __name__ == '__main__': 
    print(crawl())