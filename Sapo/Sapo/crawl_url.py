from selenium import webdriver
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
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import pandas as pd
import os
from selenium.webdriver.common.keys import Keys


options = Options()
options.add_argument("--no-sandbox")
# options.add_argument("--headless")     
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")

driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )
driver.get(
        "https://www.sapo.vn/khach-hang.html"
    )
nganh_hang = driver.find_element(By.XPATH, "//div[@class='box-filter box-filter-industry box-filter-click']/div[@class='show-filter d-md-block d-none']").click()
driver.find_element(By.XPATH, "/div[@class='group-search-industry']/ul[@class='filter-group group-industry']/li[5]/label").click()
# select_1= Select(nganh_hang)
# list_product = []

# for opt in select_1.options:
#     list_product.append(opt.text)
# print(list_product)
time.sleep(10)