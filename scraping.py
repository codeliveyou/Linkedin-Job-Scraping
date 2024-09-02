import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import date, datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import time
import os
import pandas as pd
import csv

from config import *
from setting import *
keywords = ['software developer', 'manage', 'team', 'organization', 'service', 'power', 'servant', 'control', 'steward', 'govern']

wait_time = 5

if __name__ == '__main__':
    profile_id = fnGetUUID()
    port = get_debug_port(profile_id)
    driver = get_webdriver(port)
    # driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install())

    # Set personal info to use on linkedin.
    email = LINKEDIN_EMAIL_ADDRESS
    password = LINKEDIN_EMAIL_PASSWORD

    #Sign in linkedin with email address and password.
    # driver.get('https://www.linkedin.com/checkpoint/lg/sign-in-another-account')
    # input_email = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]'))).send_keys(email)
    # input_password = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))).send_keys(password)
    # signin = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'))).click()
    # time.sleep(1)


    driver.get('https://www.linkedin.com/jobs/')
    time.sleep(1)

    job_title = "computer vision engineer"
    
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//input[@class="jobs-search-box__text-input jobs-search-box__keyboard-text-input jobs-search-global-typeahead__input"]'))).send_keys(job_title)
    time.sleep(0.9)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//input[@class="jobs-search-box__text-input jobs-search-box__keyboard-text-input jobs-search-global-typeahead__input jobs-search-box__text-input--with-clear"]'))).send_keys(Keys.ENTER)
    print('Succesed filtering job title')
    time.sleep(10)



    for x in range(10):
        tmp = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f"//ul[@class='scaffold-layout__list-container']/li[{x}]")))
        print('Current ember id : ', tmp.get_attribute('id'))
        current_ember_id = int(tmp.get_attribute('id')[5:])

        current_job_title = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f"//a[@id='{'ember' + str(current_ember_id + 6)}']/span/strong"))).text
        print('Current job title is : ', current_job_title)
        time.sleep(wait_time)
        
        current_company_name = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f"//div[@id='{'ember' + str(current_ember_id + 7)}']/span"))).text
        print('Current company name is : ', current_company_name)
        time.sleep(wait_time)
        
        current_job_detail = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//div[@class="job-details-module__content"]'))).text
        print('Current job detail : ', current_job_detail)
        time.sleep(wait_time)

        current_requirement_skills = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//a[@class="app-aware-link  job-details-how-you-match__skills-item-subtitle t-14 overflow-hidden"]'))).text
        print('Current job requirement skills : ', current_requirement_skills)
        time.sleep(wait_time)

        current_company_url = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//div[@class="job-details-jobs-unified-top-card__company-name"]/a'))).get_attribute('href')
        print('Current company url : ', current_company_url)
        time.sleep(wait_time)

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//div[@class="job-details-jobs-unified-top-card__company-name"]'))).click()
        print(f'Current we are in {current_company_name} page.')
        time.sleep(wait_time)


        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//a[@href="/company/evona-space/people/"]'))).click()
        print(f'Current we are in {current_company_name} people page.')
        time.sleep(wait_time)
        driver.refresh()
        print("Refreshed")
        time.sleep(wait_time)

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//button[@class="org-people__show-more-button t-16 t-16--open t-black--light t-bold"]'))).click()
        print(f'Extanded {current_company_name} people.')
        time.sleep(wait_time)

        people_count_elements = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[@class="org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-black--light t-normal"]/strong')))
        time.sleep(wait_time)
        people_count = []
        for element in people_count_elements:
            people_count.append(int(element.text))
        print('People Counts list Length: ', len(people_count))

        
        country_name_elements = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, f'//div[@class="org-people-bar-graph-element__percentage-bar-info truncate full-width mt2 mb1 t-14 t-black--light t-normal"]/span')))
        time.sleep(wait_time)
        country_names = []
        for element in country_name_elements:
            country_names.append(element.text)
        print('Country List Length : ', len(country_names))

        current_company_people_number = 0
        for i in range(min(len(people_count), len(country_names))):
            if country_names[i] == 'United States':
                current_company_people_number = people_count[i]
                break
        
        print(f'There are {current_company_people_number} US people are in {current_company_name}')

        time.sleep(wait_time)
        driver.back()
        time.sleep(wait_time)
        driver.back()


    keyword = keywords[0]
    target = 1000

    path = f'./informations.csv'
    check_file = os.path.exists(path)
    if check_file:
        df = pd.read_csv(path)
        print("Current extracted data size  ", len(df))
        perfect = len(df)
    else:
        with open(path, 'w', newline='') as file:
            write = csv.writer(file)
            write.writerow(['id', 'name', 'description', 'date'])
            file.close()
        perfect = 0

    driver.get('https://linkedin.com/feed')
    time.sleep(3)

    driver.get('https://www.linkedin.com/search/results/content/?keywords=software%20developer&origin=SWITCH_SEARCH_VERTICAL&sid=lAJ')
    while True:
        WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, '/html/body'))).send_keys(Keys.END)
        time.sleep(1)
        try:
            WebDriverWait(driver, 20).util(EC.visibility_of_element_located((By.XPATH, '//button[@class="artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button"]'))).click()
            print("Clicked button")
        except:
            print("No button")
        # time.sleep(1)

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="global-nav-typeahead"]/input'))).send_keys(keyword)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="global-nav-typeahead"]/input'))).send_keys(Keys.ENTER)
    
    for button_id in range(1, 10):
        if WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="search-reusables__filters-bar"]/ul/li[{button_id}]/button'))).text == "Posts":
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="search-reusables__filters-bar"]/ul/li[{button_id}]/button'))).send_keys(Keys.ENTER)
            break
        time.sleep(wait_time)

    print("extracted data number is ", perfect)

    current_id = 0

    with open(path, 'a',newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        
        for lump in range(1, 100000):
            wait_time = 10
            while wait_time < 30:
                try:
                    WebDriverWait(driver, 50).until(EC.visibility_of_all_elements_located((By.XPATH, f'//div[@class="scaffold-finite-scroll__content"]/div[{lump}]')))
                    print("sucess lump ", lump)
                    break
                except:
                    time.sleep(1)
                    WebDriverWait(driver, 50).until(EC.visibility_of_element_located((By.XPATH, '/html/body'))).send_keys(Keys.END)
                    print("wait for 10 seconds")
                    time.sleep(wait_time)
                    wait_time += 1
            if wait_time == 30:
                print("The scraping was completed.")
                break
            for k in range(1, 11):
                print(lump, k)
                try:
                    name = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f"//div[@class='scaffold-finite-scroll__content']/div[{lump}]/div/ul/li[{k}]/div/div/div/div[2]/a/div[3]/span[1]/span[1]/span[1]"))).text
                    print("name   ", name)
                    current_id += 1
                except:
                    break

                if current_id <= perfect:
                    continue

                try:
                    description = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f"//div[@class='scaffold-finite-scroll__content']/div[{lump}]/div/ul/li[{k}]/div/div/div/div[4]/div/div/span/span"))).text
                    description = description.replace('\n', ' ')
                except:
                    description = ""
                    print("empty description")
                
                try:
                    ago = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f"//div[@class='scaffold-finite-scroll__content']/div[{lump}]/div/ul/li[{k}]/div/div"))).get_attribute("data-urn")
                    posted = datetime.fromtimestamp(int((str(bin(int(ago[-19:])))[2:43]), 2) / 1000).strftime("%m/%d/%Y-%H:%M:%S")
                    print(posted)
                except:
                    posted = ""
                    print("empty date")

                if current_id == perfect + 1:
                    print("current number of extracted post is ", current_id)
                    print(perfect, name, description, posted)
                    writer.writerow([perfect, name, description, posted])
                    perfect += 1
                if perfect == target:
                    break
                time.sleep(1)
            if perfect == target:
                break
