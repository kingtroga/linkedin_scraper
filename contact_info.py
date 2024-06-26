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

# Load the Lead Profiles
DATA_FRAME = pd.read_excel('scrape_output1.xlsx')
LEAD_PROFILE_LINKS = DATA_FRAME['Linkedin URL'].tolist()
#print("Lead Profile links: ", LEAD_PROFILE_LINKS[0:2])

about_info_list = []

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
    for lead_profile in LEAD_PROFILE_LINKS:
        driver.get(lead_profile) #LEAD_PROFILE_LINKS[2])
        time.sleep(1)

        # Extract About info.
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='About']")))
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()='About']")))
            print("This user has About info")
        except Exception as e:
            print("This user has no About info")
            element = False
        finally:
            time.sleep(1)
            if element:
                try:
                    button = element.find_element(By.XPATH, "//button[text()='…Show more']")
                except Exception as e:
                    pass
                else:
                    time.sleep(1)
                    button.click()
                    time.sleep(1)
                finally:
                    section = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "about-section")))
                    about_info = section.text.strip().replace('Show less', '').replace('About\n', '')
            else:
                about_info = "NULL"

            about_info_list.append(about_info)

    #print(about_info_list)
    data = {
                'Name': DATA_FRAME['Name'].tolist(),
                'Linkedin URL': DATA_FRAME['Linkedin URL'].tolist(),
                'About': about_info_list,
                'Role': DATA_FRAME['Role'].tolist(),
                'Company': DATA_FRAME['Company'].tolist(),
                'Company Linkedin URL': DATA_FRAME['Linkedin URL'].tolist(),
                'Geography': DATA_FRAME['Geography'].tolist(),
                'Date Added': DATA_FRAME['Date Added'].tolist(),
            }
    df_about_updated = pd.DataFrame(data)
    df_about_updated.to_csv('scrape_output_about.csv')


if __name__ == "__main__":
    main()