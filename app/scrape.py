from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 
import numpy as np 
import time 
from fake_useragent import UserAgent
import os
from selenium.webdriver.chrome.options import Options


def get_title(element):
    titles = []
    for m in element:
        try:
            titles.append(m.find_element(By.XPATH,'.//div[@class="yuRUbf"]//h3 | .//h3' ).text)
        except:
            titles.append(np.nan)
    return titles


##get links
def get_link(element):
    links = []
    for m in element:
        try:
            links.append((m.find_element(By.XPATH,'.//div[@class="yuRUbf"]//a | .//a').get_attribute('href')))
        except:
            links.append(np.nan)
    return links


##get descriptions
def get_desc(element):
    desc = []
    for m in element:
        try:
            desc.append(m.find_element(By.XPATH,'.//div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc"] | .//div[@class="VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf"] |  .//div[@class="zz3gNc"]').text)
        except:
            desc.append(np.nan)      
    return desc 


##dont actually need to create this function
def get_search_topic(element,searchKey):
    search_topic = []
    for m in element:
        search_topic.append(searchKey)
    return search_topic



def scraper(searchKey,search_count,unique_table_name):
    links = []
    titles = []
    desc = []
    search_titles = []
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    chrome_options = Options()

    # chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.google.com")
    driver.set_window_size(1550, 926)
    try:
        element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH,'//div/input[1]'))
        )
        element.send_keys(searchKey)
        element.send_keys(Keys.RETURN)
        time.sleep(5)
        entire_body = driver.find_element(By.TAG_NAME,'html')
        pageHeight = driver.execute_script("return document.body.scrollHeight")

        base_directory = f'./Screenshot/{unique_table_name}'
        try:
            os.mkdir(base_directory)
        except:
            pass
        image_dir = f'{searchKey}'
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
            # print(totalScrolledHeight,pageHeight)   
            if(totalScrolledHeight+1 > pageHeight):
                break
        driver.set_window_size(1920, pageHeight)
        driver.save_screenshot(f"{final_path}/full_page.png")
        main=driver.find_elements(By.XPATH,'//div[@jscontroller="SC7lYd"] | //div[@class="usJj9c"] ')
        links = get_link(main)
        desc = get_desc(main)
        titles = get_title(main)
        search_titles = get_search_topic(main, searchKey)

        csv_dir = './CSV'
        try:
            os.mkdir(csv_dir)
        except:
            pass 

        if search_count != 0:
            df = pd.DataFrame(list(zip(search_titles, titles,links,desc,)))
            df.to_csv(f'./{csv_dir}/data_file.csv',mode='a',header=False,index=False)
        else:
            df = pd.DataFrame(list(zip(search_titles, titles,links,desc)),columns=['SearchKey','Title','Link','Desc'])
            df.to_csv(f'./{csv_dir}/data_file.csv',index=False)
    except:
        driver.quit()
    finally:
        driver.quit()
    return links,desc,titles,search_titles
