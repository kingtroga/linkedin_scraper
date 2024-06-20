import asyncio
import os
import re
from pyppeteer import launch
from pyppeteer.errors import TimeoutError as TitError

async def main():
    # Launch the browser with Tor proxy settings
    """ browser = await launch({
        'args': [
            '--proxy-server=socks5://127.0.0.1:9150',  # Tor proxy
            '--no-sandbox', 
            '--disable-setuid-sandbox'
        ],
        'headless': False
    }) """

    browser = await launch({'headless': False})
    """ browser = await launch({'args': ['--proxy-server=203.109.4.187:18092',
                                     '--no-sandbox', 
                                    '--disable-setuid-sandbox'], 'headless': False }) """


    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')

    # Navigate to the LinkedIn login page
    await page.goto('https://www.linkedin.com/sales/login', timeout=0)

    # Wait for the iframe to appear and get its frame
    await page.waitForSelector('iframe[title="Login screen"]')
    iframe_element = await page.querySelector('iframe[title="Login screen"]')
    frame = await iframe_element.contentFrame()

    # Wait for the username and password fields inside the iframe
    await frame.waitForSelector('input[name="session_key"]')
    await frame.waitForSelector('input[name="session_password"]')

    # Get the input elements
    username_input = await frame.querySelector('input[name="session_key"]')
    password_input = await frame.querySelector('input[name="session_password"]')

    # Type into the inputs
    await username_input.type(os.getenv('LINKEDIN_USERNAME'))
    await password_input.type(os.getenv('LINKEDIN_PASSWORD'))

    # Optionally, you can submit the form
    await frame.click('button[type="submit"]')

    # Function to check if still on the login page
    async def check_login_page():
        try:
            current_url = page.url
            if '/sales/login' in current_url:  # Adjust this condition based on your actual URL structure
                print("Go to your email and get the verification code.")
                return True
            return False
        except Exception as e:
            print(f"Error checking login page: {e}")
            return False

    # Wait for 60 seconds or until not on the login page
    await asyncio.sleep(20)
    for _ in range(60):
        if await check_login_page():
            await asyncio.sleep(300)  # Wait for 5 mins after printing message
        else:
            print('Login Successful!')
            break

    # Navigate to the desired page
    await page.goto('https://www.linkedin.com/sales/lists/people/7203399320862081025?sortCriteria=CREATED_TIME&sortOrder=DESCENDING', timeout=0)
    await asyncio.sleep(10)

    # Wait for the button to appear
    await page.waitForSelector('button[data-control-name="view_spotlight_for_type_ALL"]')

    # Get the button element
    button = await page.querySelector('button[data-control-name="view_spotlight_for_type_ALL"]')

    # Extract the number from the button's primary text
    number_element = await button.querySelector('.artdeco-spotlight-tab__primary-text')
    total_results = await page.evaluate('(element) => element.textContent', number_element)

    if total_results == "0":
        await asyncio.sleep(7200)  # 2 hours in seconds

    # Wait for all table rows to appear
    await page.waitForSelector('tr.artdeco-models-table-row')

    # Select all table rows
    rows = await page.querySelectorAll('tr.artdeco-models-table-row')

    # Iterate over each row
    for i, row in enumerate(rows):
        print("Row ", i)
        # Find the specific cell containing the button
        action_cell = await row.querySelector('td.list-people-detail-header__actions')
        
        # Find the button within the cell
        if action_cell:
            button = await action_cell.querySelector('button.artdeco-dropdown__trigger')
            if button:
                # Click the button
                await button.click()
                
                # Wait for some time to simulate processing (optional)
                await asyncio.sleep(2)

               # Now, find and click on the "Message" button in the dropdown using partial aria-label match
                dropdown_items = await action_cell.querySelectorAll('.artdeco-dropdown__item')
                for item in dropdown_items:
                    aria_label = await page.evaluate('(element) => element.getAttribute("aria-label")', item)
                    if aria_label and re.search(r'Message', aria_label):
                        await item.click()
                        print("Clicked on Message button.")
                        break  # Stop searching further

                # Wait for some time to simulate processing (optional)
                await asyncio.sleep(2)

                # Wait for message modal to appear using regex for aria-label
                await page.waitForSelector('button[data-control-name="overlay.close_overlay"]')

                # Find the close button within the message modal
                close_button = await page.querySelector('button[data-control-name="overlay.close_overlay"]')

                # Find the close button within the message modal
                close_button = await page.querySelector('button[data-control-name="overlay.close_overlay"]')

                # Click on the close button
                if close_button:
                    # Wait for element to appear in the message modal
                    try:
                        message_history = await page.waitForSelector('div._message-padding_zovuu6')
                    except TitError:
                        await close_button.click()
                        print("Closed message modal.")
                        await asyncio.sleep(2)
                        message_history = False
                    finally:
                        if message_history:
                            # Click on the button inside the message modal using regex for aria-label
                            print("Message History exists")
                            await asyncio.sleep(2)
                            await page.waitForXPath("//span[text()='Saved']")
                            span_elements = await page.xpath("//span[text()='Saved']")
                            save_button = span_elements[0]
                            await save_button.click()
                            
                            pass
                        else:
                            print(message_history)
                            await asyncio.sleep(2)

                        await close_button.click()
                        print("Closed message modal.")
                        await asyncio.sleep(2)
                    
                    
                    
                # Wait for some time to simulate processing (optional)
                await asyncio.sleep(2)


                

    # Close the browser
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
