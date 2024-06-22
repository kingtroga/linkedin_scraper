import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def launch_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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
    
    # Print session details
    print(f"Session URL: {driver.command_executor._url}")
    print(f"Session ID: {driver.session_id}")

    # Keep the browser open
    input("Press Enter to close the browser...")
    driver.quit()

if __name__ == "__main__":
    launch_driver()
