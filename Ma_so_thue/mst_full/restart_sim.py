from mst_full.spiders.mst import MstSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import numpy as np
import glob
import shutil
from selenium.webdriver.chrome.options import Options

PATH_CSV = "/Users/dinhvan/Document/Projects/crawl_data/scrapy/mst_full/Link_total.csv"
PATH_PRPOJECT = "/Users/dinhvan/Document/Projects/crawl_data/scrapy/mst_full"
PATH_SPLIT_RESULT = "/Users/dinhvan/Document/Projects/crawl_data/scrapy/mst_full/split_result"
PATH_SPLIT_URL = "/Users/dinhvan/Document/Projects/crawl_data/scrapy/mst_full/split_url"
PATH_RESULT_TEMP = "/Users/dinhvan/Document/Projects/crawl_data/scrapy/mst_full/result_temp/result_temp.csv"
NUMMBER_RECORD = 4000

def restart_sim():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-setuid-sandbox")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        chrome_options=options
    )
    driver.get(
        "http://192.168.8.1/html/index.html"
    )

    WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
                )
        ) 

    pass_elem = driver.find_element(
        By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
    pass_elem.send_keys("Qtcd@123")

    login_btn = driver.find_element(By.ID, "login_btn")
    WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(
                (By.ID, "login_btn")
                )
        )
    login_btn.click()

    WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "ic_reboot")
                )
        )
    WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, "ic_reboot")
                )
        ).click()
    WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']")
                )
        )
    WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[2]/div[@class='btn_normal_short pull-left margin_left_12']")
                )
        ).click() 
    
    WebDriverWait(driver, 600).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@id='login_password_close']/input[@id='login_password']")
                )
        )
    driver.quit()

def split_csv(path_csv_file):
    dataFrame_urls = pd.read_csv(path_csv_file, dtype = str)
    number_row = dataFrame_urls.shape[0]
    number_split = int(number_row/NUMMBER_RECORD) + 1
    
    directory_name = "split_url" 
    if not os.path.exists(PATH_PRPOJECT + '/' + directory_name):
        os.makedirs(PATH_PRPOJECT + '/' + directory_name)
    
    for i, df in enumerate(np.array_split(dataFrame_urls, number_split)):
        df.to_csv(PATH_PRPOJECT + '/' + directory_name + f"/url_{i + 1}.csv", index=False)
        
def move_csv(new_name):
    original = PATH_RESULT_TEMP
    target   = PATH_SPLIT_RESULT
    shutil.move(PATH_RESULT_TEMP,PATH_SPLIT_RESULT + '/' + new_name + '.csv')

def main():
    split_csv(PATH_CSV)
    
    # list_urls = [   'https://masothue.com/0101992921-001-chi-nhanh-tong-cong-ty-dau-tu-va-kinh-doanh-von-nha-nuoc',
    #                 'https://masothue.com/0101992921-002-chi-nhanh-mien-trung-tong-cong-ty-dau-tu-va-kinh-doanh-von-nha-nuoc-cong-ty-tnhh',
    #                 'https://masothue.com/0100107370-001-van-phong-dai-dien-tap-doan-xang-dau-viet-nam',
    #                 'https://masothue.com/0100100061-001-cong-ty-dich-vu-vat-tu-va-thuong-mai-hoa-chat',
    #                 'https://masothue.com/0100100061-002-cong-ty-phat-trien-phu-gia-va-san-pham-dau-mo',
    #                 'https://masothue.com/0100100061-004-trung-tam-thuong-mai-va-dich-vu-hoa-chat',
    #                 'https://masothue.com/0100100061-005-trung-tam-thong-tin-khoa-hoc-ky-thuat-hoa-chat'
    #                 ]
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path, "*.csv"))
    number_files = len([name for name in os.listdir(PATH_SPLIT_URL) if os.path.isfile(os.path.join(PATH_SPLIT_URL, name))])
    
    for number_file in range(1,number_files,1):
        restart_sim()
        
        df_url = pd.read_csv(PATH_SPLIT_URL + '/' + 'url_{}.csv'.format(number_file))
        list_url = df_url['url'].to_list()
        
        setting  = get_project_settings()
        process = CrawlerProcess(setting)
        process.crawl(MstSpider, start_urls = list_url)
        process.start()
        
        move_csv(number_file)
        
        
        
if __name__ == '__main__':
    main()
    # split_csv(PATH_CSV)