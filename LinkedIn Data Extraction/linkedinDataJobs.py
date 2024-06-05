import time
import pandas as pd 
import os
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 

url1='https://www.linkedin.com/jobs/search?keywords=Marketing%20Data%20Analyst&location=Berlin%2C%20Berlin%2C%20Germany&geoId=106967730&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

chrome_driver_path = r'drivers/chromedriver'
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(20)
driver.get(url1)

y = driver.find_element(By.CLASS_NAME, 'results-context-header__job-count').text
n = pd.to_numeric(y.replace(',', ''))

i = 2
while i <= int((n + 200) / 25) + 1:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    try:
        load_more_button = driver.find_element(By.XPATH, "//button[@aria-label='Load more results']")
        driver.execute_script("arguments[0].click();", load_more_button)
        time.sleep(3)
    except Exception as e:
        print(f"No more load button found: {e}")
        break


companyname= []
titlename= []

try:
    company_elements = driver.find_elements(By.CLASS_NAME, 'base-search-card__subtitle')
    for company_element in company_elements:
        companyname.append(company_element.text)
except Exception as e:
    print(f"Error extracting company names: {e}")

        
try:
    title_elements = driver.find_elements(By.CLASS_NAME, 'base-search-card__title')
    for title_element in title_elements:
        titlename.append(title_element.text)
except Exception as e:
    print(f"Error extracting job titles: {e}")

    
companyfinal=pd.DataFrame(companyname,columns=["company"])
titlefinal=pd.DataFrame(titlename,columns=["title"])
x=companyfinal.join(titlefinal)
x.to_csv('linkedin.csv',index=False)

try:
    job_elements = driver.find_elements(By.CLASS_NAME, 'base-card__full-link')
    hrefList = [job_element.get_attribute('href') for job_element in job_elements]
    linklist = pd.DataFrame(hrefList, columns=["joblinks"])
    linklist.to_csv('linkedin_job_links.csv', index=False)
except Exception as e:
    print(f"Error extracting job links: {e}")

    
driver.close()

