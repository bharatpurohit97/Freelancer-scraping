"""


Requirement : bs4, urllib, selenium
Edit path of chrome driver and csv file name

"""



from bs4 import BeautifulSoup
import urllib.request
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.request import urlopen as uReq
import re
import requests




def getTextFromURL(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    text = ' '.join(map(lambda p: p.text, soup.find_all('html')))
    return text


links = []
names=[]
emails=[]
phones = []


#links of location A-Z
alphabet = string.ascii_uppercase
base_url = "http://ifp.mychild.gov.au/Search/AZSearch.aspx?Location="
alphabet_link=[]
for alpha in alphabet:
    alpha_link = base_url + alpha
    alphabet_link.append(alpha_link)




for alpha_ in alphabet_link:
    resp = urllib.request.urlopen(alpha_)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        links.append(link['href'])

        
#all locations in a-z        
selected_locations = []
for location in links:
    if location.find("SearchChildcareQuickFind?location")!= -1:
        selected_locations.append(location)
        
        
baseurl = "http://ifp.mychild.gov.au/"

url_list = []

for l in selected_locations:
    urls = baseurl + l
    url_list.append(urls)

    
    

selected_page = []

driver = webdriver.Chrome(executable_path='/home/admin2/chromedriver')

for locations in url_list:
    driver.get(locations)

    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        if elem.get_attribute('href').find("ShowChildCareProvider")!= -1 and elem.get_attribute('href').find("defaultTab")==-1:
            print (elem.get_attribute("href"))
            selected_page.append(elem.get_attribute('href'))
driver.quit()







#write to csv
i = 0
filename = "myresult.csv"
f = open(filename,"w")
headers = "Emails, Names, Phone \n"
f.write(headers)

#remove duplicate pages
unique_web_pages = set(selected_page)

for p in unique_web_pages:
    text = getTextFromURL(p)
    name_list = re.findall('\n\t([^ ].*)\ - mychild.gov',text)
    email_list = re.findall('Email:\n([^ ].*)\\n',text)
    phone_list = re.findall('Phone:\n([^ ].*)\\n',text)
    emails.append(email_list)
    names.append(name_list)
    phones.append(phone_list)
    print (i,p,email_list,name_list,phone_list)
    f.write(str(email_list) + "," + str(name_list) + "," + str(phone_list) + "\n")
        
f.close()
