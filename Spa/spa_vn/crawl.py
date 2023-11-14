from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
def hande_contact(list_contact):
    dict_contact = dict.fromkeys(['email','web','phone_number'])
    for method in list_contact:
        if 'tel:' in method:
            dict_contact['phone_number'] = method
        if 'mailto' in method:
            dict_contact['email'] = method
        if 'http' in method:
            dict_contact['web'] = method
    return dict_contact
    
def check_exists_by_xpath(browser,xpath):
    try:
        browser.find_element(By.XPATH,xpath)
    except NoSuchElementException:
        return False
    return True
  
def crawl(path):
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()), 
        chrome_options= options
    )

    driver.get(
        path
    )
    try:
        name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[@class='biGQs _P fiohW eIegw']"))
        ).text
        time.sleep(2)
        if check_exists_by_xpath(driver,"//div[@class='wgNTK']/div[@class='MJ']//span[@class='biGQs _P XWJSj Wb']"):
            address = driver.find_element(By.XPATH,"//div[@class='wgNTK']/div[@class='MJ']//span[@class='biGQs _P XWJSj Wb']").text
        else:
            address = None
            
        list_contact = driver.find_elements(By.XPATH,"//div[@class='WoBiw Q3 K']/a[@class='UikNM _G B- _S _T c G_ y wSSLS wnNQG raEkE']")
        list_contact = [el.get_attribute('href') for el in list_contact]
        # time.sleep(2)
        email = hande_contact(list_contact)['email']
        phone_number = hande_contact(list_contact)['phone_number']
        web = hande_contact(list_contact)['web']
        
        dict_result = {'name':name,
                       'address':address,
                       'email':email,
                       'phone_number':phone_number,
                       'web': web,
                       }
        data = pd.DataFrame([dict_result])
        path_data = '/Users/dinhvan/Projects/Code/web_scraping/scrapy/Spa/spa_vn/spa_vn.csv'
        data.to_csv(path_data, mode='a', header=not os.path.exists(path_data), index = False)
        # data.to_csv('/Users/dinhvan/Projects/Code/web_scraping/scrapy/Spa/spa_vn/spa_vn.csv', index = False)
        print(dict_result)
        
    except Exception as e:
        print(e)
        
    driver.close()

if __name__ == '__main__':
    df_href = pd.read_csv('/Users/dinhvan/Projects/Code/web_scraping/selenium/spa_link.csv', dtype = str)
    list_path = df_href['url'].values.tolist()
    list_path = list_path[800:]
    # print(len(list_path))
    for path in list_path:  
        # path = 'https://www.tripadvisor.com.vn/Attraction_Review-g298082-d6599621-Reviews-Pandanus_Spa_Hoi_An-Hoi_An_Quang_Nam_Province.html'
        crawl(path)
        
