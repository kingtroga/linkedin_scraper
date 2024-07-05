import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import pyperclip

# Load the Lead Profiles
DATA_FRAME = pd.read_excel('scrape_output2.xlsx')

COMPANY_LEAD_PROFILE_LINKS = DATA_FRAME['Company Linkedin URL'].tolist()
#print("Company Lead Profile links: ", COMPANY_LEAD_PROFILE_LINKS[0:2])



company_headquarters_list = []
company_overiew_list = []
company_website_list = []

def main():
    # Get session details from user
    session_url = input("Enter the session URL: ")
    session_id = input("Enter the session ID: ")

    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure the browser is in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    
    # Connect to the existing browser session
    driver = webdriver.Remote(command_executor=session_url, options=chrome_options)
    driver.session_id = session_id


    # Navigate to the lead profile page and extract about_info & contact_info.
    counter = 1
    for company_profile in COMPANY_LEAD_PROFILE_LINKS:
        print(f'Getting company {counter} data')
        company_headquarters_string = ""
        company_overiew_string = ""
        company_website_string = ""


        # For some reason this person has no company 
        if pd.isna(company_profile):
            company_headquarters_string = "NULL"
            company_overiew_string = "NULL"
            company_website_string = "NULL"


            company_headquarters_list.append(company_headquarters_string)
            company_overiew_list.append(company_overiew_string)
            company_website_list.append(company_website_string)
            counter = counter + 1
            continue


        driver.get(company_profile)
        time.sleep(10)
        try:
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-control-name='read_more_description']")))
        except:
            pass
        else:
            try:
                button.click()
                time.sleep(2)
            
                company_details_modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[aria-labelledby="company-details-panel__header"]')))
            except:
                pass
            else:
                # Company overiew
                try:
                    company_overiew_string = str(company_details_modal.find_element(By.CSS_SELECTOR, 'p.company-details-panel-description').text)
                    #print("Company Overview: ", company_overiew_string)
                except:
                    pass

                # Company headquarters
                try:
                    company_headquarters_string = str(company_details_modal.find_element(By.CSS_SELECTOR, 'dd.company-details-panel-headquarters').text)
                    #print("Company headquarters: ", company_headquarters_string)
                except:
                    pass

                # Company website
                try:
                    company_website_string = str(company_details_modal.find_element(By.CSS_SELECTOR, 'a.company-details-panel-website').get_attribute('href'))
                    #print("Company Website: ", company_website_string)
                except:
                    pass
        
        if not company_headquarters_string:
            company_headquarters_string = "NULL"

        if not company_overiew_string:
            company_overiew_string = "NULL"

        if not company_website_string:
            company_website_string = "NULL"

        company_headquarters_list.append(company_headquarters_string)
        company_overiew_list.append(company_overiew_string)
        company_website_list.append(company_website_string)
        counter = counter + 1

    data = {
        'Name': DATA_FRAME['Name'].tolist(),
        'Role': DATA_FRAME['Role'].tolist(),
        'About': DATA_FRAME['About'].tolist(),
        'Linkedin URL': DATA_FRAME['Linkedin URL'].tolist(),
        'Phone(s)': DATA_FRAME['Phone(s)'].tolist(),
        'Email(s)': DATA_FRAME['Email(s)'].tolist(),
        'Website(s)': DATA_FRAME['Website(s)'].tolist(),
        'Social(s)': DATA_FRAME['Social(s)'].tolist(),
        'Address(s)': DATA_FRAME['Address(s)'].tolist(),
        'Geography': DATA_FRAME['Geography'].tolist(),
        'Date Added': DATA_FRAME['Date Added'].tolist(), 
        'Company': DATA_FRAME['Company'].tolist(),
        'Company Overview': company_overiew_list,
        'Company Headquarters': company_headquarters_list,
        'Company Website': company_website_list,
    }

    df_about_updated = pd.DataFrame(data)
    df_about_updated.to_excel('scrape_output3.xlsx', index=False)

    

    


if __name__ == "__main__":
    main()

