import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

DATA_FRAME = pd.read_excel('scrape_output3.xlsx')
COMPANY_WEBSITES = DATA_FRAME['Company Website'].tolist()
email_list = []

def extract_emails(soup):
    # Regular expression for matching emails
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    emails = set()

    # Find all mailto: links
    for mailto in soup.find_all('a', href=True):
        if mailto['href'].startswith('mailto:'):
            emails.add(mailto['href'][7:])

    # Find all text that matches the email pattern
    for text in soup.stripped_strings:
        if re.fullmatch(email_pattern, text):
            emails.add(text)

    return emails

def find_contact_page_links(soup):
    contact_links = set()
    for link in soup.find_all('a', href=True):
        if 'contact' in link['href'].lower():
            contact_links.add(link['href'])
    return contact_links

def get_soup_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def main():
    for i, url in enumerate(COMPANY_WEBSITES):
        print(f"Processing {i + 1}/{len(COMPANY_WEBSITES)}: {url}")
        email_string = ""

        soup = get_soup_from_url(url)
        if not soup:
            print("Email not found")
            email_string = "NULL"
            email_list.append(email_string)
            continue

        # Extract emails from the main page
        emails = extract_emails(soup)
        for email in emails:
            email_string = email_string + " " + str(email) + ";"
        print(f"Emails found on the main page: {email_string}")


        # Find contact page links and extract emails from them
        contact_links = find_contact_page_links(soup)
        for link in contact_links:
            if link.startswith('/'):
                contact_url = url.rstrip('/') + link
            else:
                contact_url = link
            print(f"Checking contact page: {contact_url}")
            contact_soup = get_soup_from_url(contact_url)
            if contact_soup:
                contact_emails = extract_emails(contact_soup)
                
                for email in contact_emails:
                    email_string = email_string + " " + str(email) + ";"
                print(f"Emails found on contact page {contact_url}:  {email_string}")

        if "@" not in email_string:
            email_string = "NULL"

        email_list.append(email_string)


    
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
            'Company Overview': DATA_FRAME['Company Overview'].tolist(),
            'Company Headquarters': DATA_FRAME['Company Headquarters'].tolist(),
            'Company Website': DATA_FRAME['Company Website'].tolist(),
            'Company Email Scrapes':  email_list
        }
    df_final = pd.DataFrame(data)
    df_final.to_excel('scrape_output_final.xlsx', index=False)

if __name__ == "__main__":
    main()

