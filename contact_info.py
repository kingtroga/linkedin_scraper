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
DATA_FRAME = pd.read_excel('scrape_output1.xlsx')
LEAD_PROFILE_LINKS = DATA_FRAME['Linkedin URL'].tolist()
#print("Lead Profile links: ", LEAD_PROFILE_LINKS[0:2])



socials_info_list = []
emails_info_list = []
website_info_list = []
about_info_list = []
address_info_list = []
phone_info_list = []
linkedin_profile_list = []


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
        print('Getting lead')
        time.sleep(10)

        # Extract Lead Linkedin link
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-x--lead-actions-bar-overflow-menu][aria-label="Open actions overflow menu"]')))
            button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-x--lead-actions-bar-overflow-menu][aria-label="Open actions overflow menu"]')))
        except:
            linkedin_profile_list.append("NULL")
        else:
            button.click()
            time.sleep(2)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Copy LinkedIn.com URL']")))
            copy_link_profile_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Copy LinkedIn.com URL']")))
            copy_link_profile_button.click()
            time.sleep(2)
            link_profile = pyperclip.paste()
            #print("Profile link:", link_profile)
            linkedin_profile_list.append(link_profile)

    


        # Extract Lead contact info
        socials_string = ""
        emails_string = ""
        phones_string = ""
        website_string = ""
        address_string= ""
        

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section[data-sn-view-name="lead-contact-info"]')))
            time.sleep(2)
            contact_info_section = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section[data-sn-view-name="lead-contact-info"]')))
            
            links = contact_info_section.find_elements(By.TAG_NAME, 'a')
            links = [link.get_attribute('href') for link in links if "https://www.bing.com/search?" not  in link.get_attribute('href')]
        except:
            links = []

        
        if links:
            buttons = contact_info_section.find_elements(By.TAG_NAME, 'button')
            if buttons:
                for button in buttons:
                    if "Show all" in button.text:
                        # Click the button if found
                        button.click()
                        time.sleep(2)
                        break
                try:
                    contact_info_modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.artdeco-modal__content')))
                    contact_info_modal_close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test-modal-close-btn]')))
                except:
                    print("Modal not found")
                    contact_info_modal = False
                finally:
                    if contact_info_modal:
                        # Phone(s)
                        phone_section = contact_info_modal.find_element(By.CSS_SELECTOR, 'section.contact-info-form__phone')
                        phone_section_links = phone_section.find_elements(By.TAG_NAME, 'a')
                        if phone_section_links:
                            for phone_number in phone_section_links:
                                if "tel:" in str(phone_number.get_attribute('href')):
                                    phones_string = phones_string + " " + str(phone_number.get_attribute('href')).strip().replace('tel:', ' ') + ";"
                                else:
                                    phones_string = phones_string + " " + str(phone_number.get_attribute('href')).strip().replace('tel:', ' ') + ";"

                        # Email(s)
                        email_section = contact_info_modal.find_element(By.CSS_SELECTOR, 'section.contact-info-form__email')
                        email_section_links = email_section.find_elements(By.TAG_NAME, 'a')
                        if email_section_links:
                            for email in email_section_links:
                                if "mailto:" in str(email.get_attribute('href')):
                                    emails_string = emails_string + " " + str(email.get_attribute('href')).strip().replace('mailto:', '') + ";"
                                else:
                                    emails_string = emails_string + " " + str(email.get_attribute('href')).strip().replace('mailto:', '') + ";"


                        # Website(s)
                        website_section = contact_info_modal.find_element(By.CSS_SELECTOR, 'section.contact-info-form__website')
                        website_section_links = website_section.find_elements(By.TAG_NAME, 'a')
                        if website_section_links:
                            for website in website_section_links:
                                website_string = website_string + " " + str(website.get_attribute('href')).strip() + ";"


                        # Social(s)
                        socials_section = contact_info_modal.find_element(By.CSS_SELECTOR, 'section.contact-info-form__social')
                        socials_section_links = socials_section.find_elements(By.TAG_NAME, 'a')
                        if socials_section_links:
                            for social in socials_section_links:
                                if "https://www.twitter.com/" in str(social.get_attribute('href')):
                                    socials_string = socials_string + " " + str(social.get_attribute('href')).strip() + ";"
                                elif "https://www.x.com/" in str(social.get_attribute('href')):
                                    socials_string = socials_string + " " + str(social.get_attribute('href')).strip() + ";"
                                elif "https://www.instagram.com/" in str(social.get_attribute('href')):
                                    socials_string = socials_string + " " + str(social.get_attribute('href')).strip() + ";"
                                elif "https://www.facebook.com/" in str(social.get_attribute('href')):
                                    socials_string = socials_string + " " + str(social.get_attribute('href')).strip() + ";"
                                elif "https://www.pinterest.com/" in str(social.get_attribute('href')):
                                    socials_string = socials_string + " " + str(social.get_attribute('href')).strip() + ";"
                                else:
                                    socials_string = socials_string + " " + str(social.get_attribute('href')).strip() + ";"


                        # Address(s)
                        address_section = contact_info_modal.find_element(By.CSS_SELECTOR, 'section.contact-info-form__address')
                        address_section_links = address_section.find_elements(By.TAG_NAME, 'a')
                        if address_section_links:
                            for address in address_section_links:
                                address_string = address_string + " " + str(address.get_attribute('href')).strip() + ";"
                        contact_info_modal_close_button.click()
                        time.sleep(2)
                    else:
                        for link in links:
                            # Social(s)
                            if "https://www.twitter.com/" in link:
                                socials_string = socials_string + " " + link.strip() + ";"
                            elif "https://www.x.com/" in link:
                                socials_string = socials_string + " " + link.strip() + ";"
                            elif "https://www.instagram.com/" in link:
                                socials_string = socials_string + " " + link.strip() + ";"
                            elif "https://www.facebook.com/" in link:
                                socials_string = socials_string + " " + link.strip() + ";"
                            elif "https://www.pinterest.com/" in link:
                                socials_string = socials_string + " " + link.strip() + ";"
                            # Email(s)
                            elif "mailto:" in link:
                                emails_string = emails_string + " " + link.strip().replace('mailto:', '') + ";"
                            # Phone(s)
                            elif "tel:" in link:
                                phones_string = phones_string + " " + link.strip().replace('tel:', ' ') + ";"
                            else:
                                website_string = website_string + " " + link.strip() + ";"

        else:
            print("This user has no contact infomation on their linkedin sales nav profile")
        time.sleep(2)

        # Check if any string is empty, if it is...set it to NULL
        if not socials_string:
            socials_string = "NULL"

        if not emails_string:
            emails_string = "NULL"
            
        if not phones_string:
            phones_string = "NULL"
            
        if not website_string:
            website_string = "NULL"
            
        if not address_string:
            address_string = "NULL"

        socials_info_list.append(socials_string)
        emails_info_list.append(emails_string)
        website_info_list.append(website_string)
        address_info_list.append(address_string)
        phone_info_list.append(phones_string)
    

        # Test
        """ data = {
                'Name': DATA_FRAME['Name'].tolist(),
                'Role': DATA_FRAME['Role'].tolist(),
                #'About': about_info_list,
                'Linkedin URL': DATA_FRAME['Linkedin URL'].tolist(),
                'Phone(s)': phone_info_list,
                'Email(s)': emails_info_list,
                'Website(s)': website_info_list,
                'Social(s)': socials_info_list,
                'Address(s)': address_info_list,
                'Geography': DATA_FRAME['Geography'].tolist(),
                'Date Added': DATA_FRAME['Date Added'].tolist(), 
                'Company': DATA_FRAME['Company'].tolist(),
                'Company Linkedin URL': DATA_FRAME['Linkedin URL'].tolist(),

            }
        df_about_updated = pd.DataFrame(data)
        df_about_updated.to_csv('scrape_output_contact_info.csv') """


        # Extract Lead About info.
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

        # Test
        """ #print(about_info_list)
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
 """
    data = {
        'Name': DATA_FRAME['Name'].tolist(),
        'Role': DATA_FRAME['Role'].tolist(),
        'About': about_info_list,
        'Linkedin URL': linkedin_profile_list,
        'Phone(s)': phone_info_list,
        'Email(s)': emails_info_list,
        'Website(s)': website_info_list,
        'Social(s)': socials_info_list,
        'Address(s)': address_info_list,
        'Geography': DATA_FRAME['Geography'].tolist(),
        'Date Added': DATA_FRAME['Date Added'].tolist(), 
        'Company': DATA_FRAME['Company'].tolist(),
        'Company Linkedin URL': DATA_FRAME['Linkedin URL'].tolist(),
    }
    df_about_updated = pd.DataFrame(data)
    df_about_updated.to_excel('scrape_output2.xlsx', index=False)

if __name__ == "__main__":
    main()