import asyncio
import os
from pyppeteer import launch

async def main():
    browser = await launch(headless=False)
    #browser = await launch({'args': ['--proxy-server=221.140.235.236:5002'], 'headless': False })
    page = await browser.newPage()

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
    for i,row in enumerate(rows):
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

    # Close the browser
    await browser.close()

asyncio.run(main())
