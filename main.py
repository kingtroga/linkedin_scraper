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


def main():

    # Navigate to the LinkedIn login page
    driver.get('https://www.linkedin.com/sales/login')

    # Wait for the iframe to appear and switch to its context
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="Login screen"]')))

    # Wait for the username and password fields inside the iframe
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'session_key')))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'session_password')))

    # Get the input elements
    username_input = driver.find_element(By.NAME, 'session_key')
    password_input = driver.find_element(By.NAME, 'session_password')

    # Type into the inputs
    username_input.send_keys(os.getenv('LINKEDIN_USERNAME'))
    password_input.send_keys(os.getenv('LINKEDIN_PASSWORD'))

    # Submit the form
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Function to check if still on the login page
    def check_login_page():
        try:
            current_url = driver.current_url
            if '/sales/login' in current_url:
                print("Go to your email and get the verification code Or solve the AUDIO challenge and wait for the page to load")
                return True
            return False
        except Exception as e:
            print(f"Error checking login page: {e}")
            return False

    # Wait for 60 seconds or until not on the login page
    time.sleep(20)
    for _ in range(60):
        if check_login_page():
            time.sleep(120)
        else:
            print('Login Successful!')
            break

    # Navigate to the desired page
    driver.get('https://www.linkedin.com/sales/lists/people/7203399320862081025?sortCriteria=CREATED_TIME&sortOrder=DESCENDING')
    time.sleep(10)

    coconut = True

    while coconut:
        # Wait for the button to appear
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-control-name="view_spotlight_for_type_ALL"]')))

        # Get the button element
        button = driver.find_element(By.CSS_SELECTOR, 'button[data-control-name="view_spotlight_for_type_ALL"]')

        # Extract the number from the button's primary text
        number_element = button.find_element(By.CSS_SELECTOR, '.artdeco-spotlight-tab__primary-text')
        total_results = number_element.text

        print("Total_results: ", total_results)

        if total_results == "0":
            print("Nobody to reach out to hence this program will sleep for the next two hours")
            time.sleep(7200)  # 2 hours in seconds
        else:
            # Wait for all table rows to appear
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.artdeco-models-table-row')))

            # Select all table rows
            rows = driver.find_elements(By.CSS_SELECTOR, 'tr.artdeco-models-table-row')

            # Iterate over each row
            for i, row in enumerate(rows):
                print("Row ", i)
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
                                time.sleep(2)

                            # Remove from "Need to reach out to" List
                            save_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Saved']")))
                            save_button.click()
                            time.sleep(2)

                            remove_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Need to Reach out To']")))
                            remove_button.click()
                            time.sleep(2)

                            # Add to Emailed list
                            emailed_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Emailed']")))
                            emailed_button.click()

                            close_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[data-control-name="overlay.close_overlay"]')))
                            close_button.click()
                            print("Closed message modal.")
                            time.sleep(2)

        driver.refresh()
        time.sleep(10)
        print('Page Reloaded successfully. Resuming Task...')

if __name__ == "__main__":
    main()
