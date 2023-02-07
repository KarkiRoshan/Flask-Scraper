from selenium import webdriver
from selenium.webdriver.common.keys import Keys   ##gives acces to certain keys
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
import argparse
import numpy as np
from selenium.webdriver.chrome.options import Options
import os


def daraz_crawler(item_name,count,unique_table_name):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.daraz.com.np")
    driver.set_window_size(1550, 926)
    try:
        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//div//input[@id="q"]'))
        )
        element.send_keys(item_name)
        element.send_keys(Keys.RETURN)
        main=driver.find_elements(By.XPATH,'//div[@class="box--pRqdD"]')
        time.sleep(2)
        pageHeight = driver.execute_script("return document.body.scrollHeight")
        entire_body = driver.find_element(By.TAG_NAME,'body')
        pageHeight = driver.execute_script("return document.body.scrollHeight")
       
        base_directory = f'./Screenshot/{unique_table_name}'
        try:
            os.mkdir(base_directory)
        except:
            pass
        image_dir = f'{item_name}'
        final_path = os.path.join(base_directory,image_dir)

        i=0
        try:
            os.mkdir(final_path)
        except:
            pass 

        totalScrolledHeight = 0 
        # print(totalScrolledHeight,pageHeight)
        while True:
            driver.save_screenshot(f'./{final_path}/{i}.png')
            entire_body.send_keys(Keys.PAGE_DOWN)
            
            totalScrolledHeight = driver.execute_script("return window.pageYOffset + window.innerHeight")
            i += 1 
            if(totalScrolledHeight+1 > pageHeight):
                break
        
       
        driver.set_window_size(1920, pageHeight)
        driver.save_screenshot(f"{final_path}/full_page.png")

        driver.set_window_size(1920, pageHeight)

        titles = []
        prices = []
        item_title = []
        for m in main:
            #title
            try:
                titles.append(m.find_element(By.XPATH,'.//div[@class="title--wFj93"]//a').text)
                    
            except:
                titles.append(np.nan) 
            #price 
            try:
                prices.append(m.find_element(By.XPATH,'.//div[@class="price--NVB62"]//span').text)
            except:
                prices.append(np.nan)
            finally:
                item_title.append(item_name)

        # print(len(titles),len(prices))
        csv_dir = './CSV'
        try:
            os.mkdir(csv_dir)
        except:
            pass 
        if count != 0:
            df = pd.DataFrame(list(zip(item_title, titles,prices)))
            df.to_csv(f'./{csv_dir}/data_file.csv',mode='a',header=False,index=False)
        else:
            df = pd.DataFrame(list(zip(item_title, titles,prices)),columns=['SearchKey','Title','Price'])
            df.to_csv(f'./{csv_dir}/data_file.csv',index=False)
            
    except:
        driver.quit()