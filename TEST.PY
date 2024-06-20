import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Set user agent
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")
    
    # Launch the browser and navigate to LinkedIn login page
    driver.get('https://www.linkedin.com/sales/login')

    # Wait for the iframe to appear and switch to it
    iframe_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="Login screen"]'))
    )
    driver.switch_to.frame(iframe_element)

    # Wait for the username and password fields inside the iframe
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'session_key'))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, 'session_password'))
    )

    # Type into the inputs
    username_input.send_keys(os.getenv('LINKEDIN_USERNAME'))
    password_input.send_keys(os.getenv('LINKEDIN_PASSWORD'))

    # Submit the form
    password_input.send_keys(Keys.RETURN)

    # Switch back to the default content
    driver.switch_to.default_content()

    # Function to check if still on the login page
    def check_login_page():
        current_url = driver.current_url
        if '/sales/login' in current_url:  # Adjust this condition based on your actual URL structure
            print("Go to your email and get the verification code.")
            return True
        return False

    # Wait for 60 seconds or until not on the login page
    time.sleep(20)
    for _ in range(60):
        if check_login_page():
            time.sleep(300)  # Wait for 5 mins after printing message
        else:
            print('Login Successful!')
            break

    # Navigate to the desired page
    driver.get('https://www.linkedin.com/sales/lists/people/7203399320862081025?sortCriteria=CREATED_TIME&sortOrder=DESCENDING')
    time.sleep(10)

    # Wait for the button to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-control-name="view_spotlight_for_type_ALL"]'))
    )

    # Get the button element
    button = driver.find_element(By.CSS_SELECTOR, 'button[data-control-name="view_spotlight_for_type_ALL"]')

    # Extract the number from the button's primary text
    number_element = button.find_element(By.CLASS_NAME, 'artdeco-spotlight-tab__primary-text')
    total_results = number_element.text

    if total_results == "0":
        time.sleep(7200)  # 2 hours in seconds

    # Wait for all table rows to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.artdeco-models-table-row'))
    )

    # Select all table rows
    rows = driver.find_elements(By.CSS_SELECTOR, 'tr.artdeco-models-table-row')

    # Iterate over each row
    for i, row in enumerate(rows):
        print("Row ", i)
        # Find the specific cell containing the button
        action_cell = row.find_element(By.CSS_SELECTOR, 'td.list-people-detail-header__actions')
        
        # Find the button within the cell
        button = action_cell.find_element(By.CSS_SELECTOR, 'button.artdeco-dropdown__trigger')
        if button:
            # Click the button
            button.click()
            
            # Wait for some time to simulate processing (optional)
            time.sleep(2)

            # Now, find and click on the "Message" button in the dropdown using partial aria-label match
            dropdown_items = action_cell.find_elements(By.CSS_SELECTOR, '.artdeco-dropdown__item')
            for item in dropdown_items:
                aria_label = item.get_attribute('aria-label')
                if aria_label and re.search(r'Message', aria_label):
                    item.click()
                    print("Clicked on Message button.")
                    break  # Stop searching further

            # Wait for some time to simulate processing (optional)
            time.sleep(2)

            # Wait for message modal to appear using regex for aria-label
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-control-name="overlay.close_overlay"]'))
            )

            # Find the close button within the message modal
            close_button = driver.find_element(By.CSS_SELECTOR, 'button[data-control-name="overlay.close_overlay"]')

            # Click on the close button
            if close_button:
                # Wait for element to appear in the message modal
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'div._message-padding_zovuu6'))
                    )
                except Exception as e:
                    close_button.click()
                    print("Closed message modal.")
                    time.sleep(2)
                    message_history = False
                else:
                    message_history = True
                    pass
                finally:
                    if message_history:
                        pass
                    else:
                        print(message_history)
                        time.sleep(2)

                    close_button.click()
                    print("Closed message modal.")
                    time.sleep(2)

            # Wait for some time to simulate processing (optional)
            time.sleep(2)

finally:
    # Close the browser
    driver.quit()
