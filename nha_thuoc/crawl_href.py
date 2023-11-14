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
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import pandas as pd
import os

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--headless")   
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
def crawl_href():
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )
    driver.get(
        'https://imiale.com/dai-ly-phan-phoi/'
    )
    time.sleep(2)
    list_href = [value.get_attribute('href') for value in driver.find_elements(By.XPATH,"//table//ul//a")]
    list_location = [value.text for value in driver.find_elements(By.XPATH,"//table//ul//a")]
    data = pd.DataFrame()
    data['href'] = pd.Series(list_href)
    data['location'] = pd.Series(list_location)
    
    data.to_csv('/Users/dinhvan/Projects/Code/web_scraping/scrapy/nha_thuoc/href.csv', index=False)
    driver.close()
if __name__ == '__main__':
    crawl_href()