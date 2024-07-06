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
from selenium.common.exceptions import TimeoutException as SeleniumTimeOutException
import pandas as pd


# DATA LOSS PREVENTION FOLDER
DLP_DIRECTORY = 'dlp'

def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory '{path}' created successfully or already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

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

    # Navigate to the desired page
    driver.get('https://www.linkedin.com/sales/lists/people/7209949800270548995?sortCriteria=CREATED_TIME&sortOrder=DESCENDING')
    time.sleep(10)



    coconut = True
    lead_counter = 0
    data = []

    while coconut:
        try:
            # Wait for the button to appear
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-control-name="view_spotlight_for_type_ALL"]')))

            # Get the button element
            button = driver.find_element(By.CSS_SELECTOR, 'button[data-control-name="view_spotlight_for_type_ALL"]')
            # Extract the number from the button's primary text
            number_element = button.find_element(By.CSS_SELECTOR, '.artdeco-spotlight-tab__primary-text')
            total_results = int(number_element.text)
        except Exception as e:
            total_results = 0

       
        print("Total_results: ", total_results)

        if total_results == 0:
            print("Nobody to reach out to hence this program will sleep for the next two hours")
            if data:
                df = pd.DataFrame(data)

                # Define the Excel file path
                excel_file = 'scrape_output1.xlsx'
                csv_file = 'scrape_output1.csv'

                try:
                    # Write the DataFrame to an Excel file
                    df.to_excel(excel_file, index=False)

                    # Remove duplicate rows
                    df = pd.read_excel(excel_file)
                    df_cleaned = df.drop_duplicates()
                    df_cleaned.to_excel(excel_file, index=False)


                    print(f"Data scrapped has been written to {excel_file}")
                except:
                    # If Openpxl is unavalible write the data to a CSV file
                    df.to_csv(csv_file, index=False)

                    # Remove duplicate rows
                    df = pd.read_csv(csv_file)
                    df_cleaned = df.drop_duplicates()
                    df_cleaned.to_csv(csv_file, index=False)
                    
                    print(f"Data scrapped has been written to {csv_file}")
                

            
            time.sleep(7200)  # 2 hours in seconds
        else:
            # Wait for all table rows to appear
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.artdeco-models-table-row')))
                            
            # Now get the html code
            page_source = driver.page_source

            soup = BeautifulSoup(page_source, 'html.parser')

            # Finding the table body
            table_body = soup.find('tbody')

            # Extracting rows from the table
            rows = table_body.find_all('tr')

            # List to store extracted data
            

            for i, row in enumerate(rows):
                # Extracting each cell in the row
                cells = row.find_all('td')
                
                # Extracting Name
                try:
                    name = cells[0].find('a', class_='t-bold').get_text(strip=True)
                except:
                    name = "NULL"

                try:
                    linkedin_url =  "https://www.linkedin.com" +  str(cells[0].find('a', class_='t-bold')['href'])
                except:
                    linkedin_url = "NULL"
                
                # Extracting Role
                try:
                    role = cells[0].find('div', style='display: -webkit-box; -webkit-box-orient: vertical; overflow: hidden; -webkit-line-clamp: 2; overflow-wrap: anywhere;').get_text(strip=True)
                except:
                    role = "NULL"
                
                # Extracting Company (Account)
                try:
                    company = cells[1].find('span', {'data-anonymize': 'company-name'}).get_text(strip=True)
                except:
                    company = "NULL"

                # Extracting the Company Linkedin URL
                try:
                    company_linkedin_url = "https://www.linkedin.com" +  str(cells[1].find('a', href=lambda href: href and re.search(r'/sales/company/', href))['href'])
                except:
                    company_linkedin_url = "NULL"
                
                # Extracting Geography
                try:
                    geography = cells[2].get_text(strip=True)
                except:
                    geography = "NULL"
                
                # Extracting Date Added
                try:
                    date_added = cells[5].get_text(strip=True)
                except:
                    date_added = "NULL"
                
                # Appending extracted data to the list
                data.append({
                    'Name': name,
                    'Linkedin URL': linkedin_url,
                    'Role': role,
                    'Company': company,
                    'Company Linkedin URL': company_linkedin_url,
                    'Geography': geography,
                    'Date Added': date_added
                })

            # DATA LOSS PREVENTION IS DLP LOGIC
            create_directory(DLP_DIRECTORY)
            print(f"{len(rows)} Rows of Data Scraped Successfully")

            df = pd.DataFrame(data)

            # Define the Excel file path
            excel_file = os.path.join(DLP_DIRECTORY, 'scrape_output1.xlsx')
            csv_file = os.path.join(DLP_DIRECTORY, 'scrape_output1.csv')


            try:
                # Write the DataFrame to an Excel file
                df.to_excel(excel_file, index=False)

                # Remove duplicate rows
                df = pd.read_excel(excel_file)
                df_cleaned = df.drop_duplicates()
                df_cleaned.to_excel(excel_file, index=False)

                print(f"{excel_file} has been updated")
            except:
                # If Openpxl is unavalible write the data to a CSV file
                df.to_csv(csv_file, index=False)


                # Remove duplicate rows
                df = pd.read_csv(csv_file)
                df_cleaned = df.drop_duplicates()
                df_cleaned.to_csv(csv_file, index=False)


                print(f"{csv_file} has been updated")
            



            
            # Select all table rows
            rows = driver.find_elements(By.CSS_SELECTOR, 'tr.artdeco-models-table-row')

            # Iterate over each row
            for i, row in enumerate(rows):
                restricted = None
                error_occured = None
                connected_button_click = False
                print("Lead: ", lead_counter + 1)
                # Find the specific cell containing the button
                action_cell = row.find_element(By.CSS_SELECTOR, 'td.list-people-detail-header__actions')

                # Find the button within the cell
                if action_cell:
                    button = action_cell.find_element(By.CSS_SELECTOR, 'button.artdeco-dropdown__trigger')
                    if button:
                        # Click the button
                        button.click()
                        time.sleep(2)

                        # Now, find and click on the "Message" button in the dropdown using partial aria-label match
                        dropdown_items = action_cell.find_elements(By.CSS_SELECTOR, '.artdeco-dropdown__item')
                        for item in dropdown_items:
                            aria_label = item.get_attribute('aria-label')
                            if aria_label and re.search(r'Message', aria_label):
                                item.click()
                                print("Clicked on Message button.")
                                break  # Stop searching further

                        time.sleep(2)

                        # Wait for message modal to appear using regex for aria-label
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-control-name="overlay.close_overlay"]')))

                        try:
                            message_history = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._message-padding_zovuu6')))
                        except Exception as e:
                            message_history = False
                        finally:
                            if message_history:
                                print("Message History exists")
                                time.sleep(2)
                            else:
                                print("Message History doesn't exist")
                                time.sleep(2)
                                # There is no message history so send the message
                                try:
                                    subject_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Subject (required)"]')))
                                    subject_field.send_keys("Cost Effective, Efficient, 3PL Services & Freight Forwarding Services")
                                    time.sleep(2)

                                    message_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//textarea[@placeholder="Type your message here…"]')))
                                    message_field.send_keys("""At Prime Avenue Logistics (https://primeavenuelogistics.com/), we specialize in providing top-tier 3PL solutions, including freight forwarding, pick pack ship, import/export, customs clearance, Amazon/Walmart replenishment, and warehousing services. Our straightforward pricing ensures you get value without the hassle.

    Already have a 3PL or freight forwarder? We can provide you with a free no strings attached quote.

    Let's chat about how we can streamline your supply chain and drive your success.
    """)
                                    time.sleep(2)

                                    send_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Send']")))
                                    send_button.click()
                                    time.sleep(5)
                                except:
                                    try:
                                        restricted = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.conversation-restriction')))
                                    except:
                                        error_occured = "True"

                            #print(error_occured, "ERROR_OCCURED")

                            if restricted != None or error_occured == "True":
                                # Close the modal
                                time.sleep(2)
                                close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-control-name="overlay.close_overlay"]')))
                                close_button.click()
                                print("Closed message modal.")
                                time.sleep(2)

                                # Open dropdown and click on connect
                                action_cell = row.find_element(By.CSS_SELECTOR, 'td.list-people-detail-header__actions')
                                try:
                                    # Find the button within the cell
                                    if action_cell:
                                        button = action_cell.find_element(By.CSS_SELECTOR, 'button.artdeco-dropdown__trigger')
                                        if button:
                                            # Click the button
                                            button.click()
                                            time.sleep(2)

                                            # Now, find and click on the "Connect" button in the dropdown using partial aria-label match
                                            dropdown_items = action_cell.find_elements(By.CSS_SELECTOR, '.artdeco-dropdown__item')
                                            for item in dropdown_items:
                                                aria_label = item.get_attribute('class')
                                                if aria_label and re.search(r'list-detail__connect-option', aria_label):
                                                    item.click()
                                                    print("Clicked on Connect button.")
                                                    connected_button_click = True
                                                    break  # Stop searching further
                                                
                                    time.sleep(2)

                                    # Send connecting message
                                    if not connected_button_click:
                                        print("You have connected with this lead before")
                                        time.sleep(2)

                                        action_cell = row.find_element(By.CSS_SELECTOR, 'td.list-people-detail-header__actions')
                                        #action_cell = row.find_element(By.CSS_SELECTOR, 'td.list-people-detail-header__actions')
                                        #print("ACTION_CELL", action_cell)

                                        # Find the button within the cell
                                        if action_cell:
                                            button = action_cell.find_element(By.CSS_SELECTOR, 'button.artdeco-dropdown__trigger')
                                            if button:
                                                # Click the button
                                                button.click()
                                                # click on the button again
                                                button.click()
                                                time.sleep(2)

                                                # Now, find and click on the "Message" button in the dropdown using partial aria-label match
                                                dropdown_items = action_cell.find_elements(By.CSS_SELECTOR, '.artdeco-dropdown__item')
                                                for item in dropdown_items:
                                                    aria_label = item.get_attribute('aria-label')
                                                    if aria_label and re.search(r'Message', aria_label):
                                                        item.click()
                                                        print("Clicked on Message button.")
                                                        break  # Stop searching further

                                                time.sleep(2)
                                        
                                        save_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Saved']")))
                                        save_button.click()
                                        time.sleep(2)

                                        remove_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Need to Reach out To']")))
                                        remove_button.click()
                                        time.sleep(2)

                                        test_list_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Connecting']")))
                                        test_list_button.click()
                                        time.sleep(2)

                                        close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-control-name="overlay.close_overlay"]')))
                                        close_button.click()
                                        print("Closed message modal.")
                                        time.sleep(2)
                                        lead_counter = lead_counter + 1
                                        continue
                                    else:
                                        connect_modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-sn-view-name="subpage-connect-modal"]')))
                                        

                                except:
                                    print("You have either Connected with this lead before or An unknown Error occured. Saving this lead to the 'Connecting' list")
                                    time.sleep(2)

                                    action_cell = row.find_element(By.CSS_SELECTOR, 'td.list-people-detail-header__actions')
                                    #action_cell = row.find_element(By.CSS_SELECTOR, 'td.list-people-detail-header__actions')

                                    # Find the button within the cell
                                    if action_cell:
                                        button = action_cell.find_element(By.CSS_SELECTOR, 'button.artdeco-dropdown__trigger')
                                        if button:
                                            # Click the button
                                            button.click()
                                            time.sleep(2)

                                            # Now, find and click on the "Message" button in the dropdown using partial aria-label match
                                            dropdown_items = action_cell.find_elements(By.CSS_SELECTOR, '.artdeco-dropdown__item')
                                            for item in dropdown_items:
                                                aria_label = item.get_attribute('aria-label')
                                                if aria_label and re.search(r'Message', aria_label):
                                                    item.click()
                                                    print("Clicked on Message button.")
                                                    break  # Stop searching further

                                            time.sleep(2)
                                    
                                    save_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Saved']")))
                                    save_button.click()
                                    time.sleep(2)

                                    remove_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Need to Reach out To']")))
                                    remove_button.click()
                                    time.sleep(2)

                                    test_list_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Info Retrieved']")))
                                    test_list_button.click()
                                    time.sleep(2)

                                    close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-control-name="overlay.close_overlay"]')))
                                    close_button.click()
                                    print("Closed message modal.")
                                    time.sleep(2)
                                    lead_counter = lead_counter + 1
                                    continue
                                else:
                                    
                                    message_box = connect_modal.find_element(By.CSS_SELECTOR, 'textarea#connect-cta-form__invitation')
                                    message_box.send_keys('I wanted to connect to see if we could offer you a more Cost Effective, Efficient, 3PL Services &/or Freight Forwarding Services (https://primeavenuelogistics.com/).')
                                    time.sleep(2)

                                    # Check if to connect with this Lead an email is needed
                                    try:
                                        email_needed = connect_modal.find_element(By.CSS_SELECTOR, 'input#connect-cta-form__email')
                                    except:
                                        email_needed = False

                                    if email_needed:
                                        print("You need this Lead's email to connect")
                                        time.sleep(2)
                                        close_connect_modal_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-test-modal-close-btn]')))
                                        close_connect_modal_button.click()
                                        # Find the button within the cell
                                        if action_cell:
                                            button = action_cell.find_element(By.CSS_SELECTOR, 'button.artdeco-dropdown__trigger')
                                            if button:
                                                # Click the button
                                                button.click()
                                                time.sleep(2)

                                                # Now, find and click on the "Message" button in the dropdown using partial aria-label match
                                                dropdown_items = action_cell.find_elements(By.CSS_SELECTOR, '.artdeco-dropdown__item')
                                                for item in dropdown_items:
                                                    aria_label = item.get_attribute('aria-label')
                                                    if aria_label and re.search(r'Message', aria_label):
                                                        item.click()
                                                        print("Clicked on Message button.")
                                                        break  # Stop searching further

                                                time.sleep(2)
                                        
                                        save_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Saved']")))
                                        save_button.click()
                                        time.sleep(2)

                                        remove_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Need to Reach out To']")))
                                        remove_button.click()
                                        time.sleep(2)

                                        test_list_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Info Retrieved']")))
                                        test_list_button.click()
                                        time.sleep(2)

                                        close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-control-name="overlay.close_overlay"]')))
                                        close_button.click()
                                        print("Closed message modal.")
                                        time.sleep(2)
                                        lead_counter = lead_counter + 1
                                        continue
                                    



                                    invitation_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Send Invitation']")))
                                    invitation_button.click()
                                    time.sleep(2)


                                    # NOW ADD THE LEAD TO THE CONNECTING LIST AND REMOVE FROM THE NEED TO REACH OUT LIST
                                    action_cell = row.find_element(By.CSS_SELECTOR, 'td.list-people-detail-header__actions')

                                    # Find the button within the cell
                                    if action_cell:
                                        button = action_cell.find_element(By.CSS_SELECTOR, 'button.artdeco-dropdown__trigger')
                                        if button:
                                            # Click the button
                                            button.click()
                                            time.sleep(2)

                                            # Now, find and click on the "Message" button in the dropdown using partial aria-label match
                                            dropdown_items = action_cell.find_elements(By.CSS_SELECTOR, '.artdeco-dropdown__item')
                                            for item in dropdown_items:
                                                aria_label = item.get_attribute('aria-label')
                                                if aria_label and re.search(r'Message', aria_label):
                                                    item.click()
                                                    print("Clicked on Message button.")
                                                    break  # Stop searching further

                                            time.sleep(2)
                                    
                                    save_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Saved']")))
                                    save_button.click()
                                    time.sleep(2)

                                    remove_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Need to Reach out To']")))
                                    remove_button.click()
                                    time.sleep(2)
                                    
                                    #TODO: Add the code for the wide Linkedin Sales Navigator error
                                    # Add to Connecting list
                                    connecting_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Connecting']")))
                                    connecting_button.click()

                                    """ # Add to test list
                                    test_list_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Test List']")))
                                    test_list_button.click() """

                                    """ # Add to Emailed list
                                    emailed_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Emailed']")))
                                    emailed_button.click() """

                                    close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-control-name="overlay.close_overlay"]')))
                                    close_button.click()
                                    print("Closed message modal.")
                                    time.sleep(2)
                                    lead_counter = lead_counter + 1
                                    continue
                                    

                            else:
                                # Remove from "Need to reach out to" List
                                save_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Saved']")))
                                save_button.click()
                                time.sleep(2)

                                remove_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Need to Reach out To']")))
                                remove_button.click()
                                time.sleep(2)
                                
                                #TODO: Add the code for the wide Linkedin Sales Navigator error
                                """ # Add to Connecting list
                                connecting_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Connecting']")))
                                connecting_button.click() """

                                """ # Add to test list
                                test_list_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Test List']")))
                                test_list_button.click() """

                                # Add to Emailed list
                                emailed_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Emailed']")))
                                emailed_button.click()

                                close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-control-name="overlay.close_overlay"]')))
                                close_button.click()
                                print("Closed message modal.")
                                time.sleep(2)
                                lead_counter = lead_counter + 1

        driver.refresh()
        time.sleep(10)
        print('Page Reloaded successfully. Resuming Task...')

if __name__ == "__main__":
    main()
