"""
Author : Rakesh Sharma, Bharat Purohit

Freelancing project

Requirement : selenium,bs4,time

Edit : 1. change path of chrome driver

"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
import re
import pandas as pd

df = pd.DataFrame(columns=['NAME','PHONE','EMAIL','ADDRESS'])
base = "//li[@class='address role-type-26' and @value = "
new_name = []
for i in range(0,1000):
    new_name.append(base + "'"+str(i)+"'" + "]")

driver = webdriver.Chrome(executable_path='/home/admin2/chromedriver') 


phone=[]
address=[]
email=[]
name=[]
base_url = "https://tallysolutions.com/website/html/partner-new/partner-search-results.php?searchEvent=1&searchBy=loc&location=India#page-1"
driver.get(base_url)
for i in range(0,10000000):
    try:
        sleep(10)
        j=0
        if j>=1 or i >=1:
           # text = driver.find_element_by_tag_name("body").get_attribute("innerText")
            button_element = driver.find_element_by_link_text('Next')
            button_element.click()
            sleep(1)
        try:
            data = ""
            k = 0
            for p in new_name:
                sleep(5)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,p))).click()
                text = driver.find_element_by_tag_name("body").get_attribute('innerHTML')
                data = str(text)
                phone.append(re.findall('<a href="tel:([0-9][^ ].*?)\">[0-9]',data))
                address.append(re.findall('style="padding:0px;"><p> ([^ ].*)\</p></div></div>',data))
                email.append(re.findall('href="mailto:([^ ].*)\ class="mail_tag"',data))
                name.append(re.findall('style="padding:0px;"><p>([^ ].*?)\</p><p>',data))
                df = df.append({'NAME':name[k],'PHONE':phone[k],'EMAIL':email[k],'ADDRESS':address[k]},ignore_index=True)
                k = k+1
        except:
            j= j+1
            pass
    except:
        driver.close()
df.to_csv("sample_Data.csv")
