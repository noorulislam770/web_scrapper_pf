import time
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os


# Configure the Selenium WebDriver (Make sure you have the ChromeDriver installed)


def configure_driver():
    chrome_options = Options()
    # Run in headless mode to avoid opening browser window
    # chrome_options.add_argument("--headless")
    # Set the correct path to your ChromeDriver
    service = Service('D:\\chromedrivers\\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to get the candidate's page link from the list


def find_candidate_page(driver, candidate_name, list_page_url):
    print(f"Navigating to the list page: {list_page_url}")
    driver.get(list_page_url)

    # Wait for the page to load and locate the list
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.TAG_NAME, 'table')))  # Adjust as per the actual structure
        print("Page loaded successfully.")
    except Exception as e:
        print("Failed to load the candidate list page:", str(e))
        return None

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the candidate's link (Assuming the names are within <a> tags in a table)
    for link in soup.find_all('a'):
        if candidate_name.lower() in link.text.lower():
            candidate_url = link.get('href')
            print(
                f"Candidate '{candidate_name}' found. Navigating to the detailed page.")
            return candidate_url

    print(f"Candidate '{candidate_name}' not found.")
    return None

# Function to extract candidate details from their page


def extract_candidate_details(driver, candidate_url):
    print(f"Navigating to candidate's page: {candidate_url}")
    driver.get(candidate_url)

    # Wait for the page to load
    time.sleep(2)  # A more robust solution should use WebDriverWait

    # Parse the page source
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract details (this part depends on the exact structure of the candidate's page)
    # You need to adjust the selectors according to the website's actual layout
    details = {
        "name": soup.find('h2', {'class': 'profile-name'}).text.strip(),
        "contact_info": extract_contact_info(soup),
        "email" : extract_email_info(soup),
        "occupation": extract_occupation(soup),
        "family_details(father/spouce)": extract_family_details(soup),
        "political_party_affiliation": extract_political_affiliation(soup),
        "images": extract_images(soup)
    }

    print("Details extracted successfully.")
    return details



def extract_email_info(soup):
    posts_text_divs = soup.find_all('div', {'class': 'posts_text'})

    # Check if there are at least two div elements with the class posts_text
    if len(posts_text_divs) >= 2:
        # Extract the text from the second div element
        email = posts_text_divs[2]
        # Remove any unnecessary tags and text
        for br in email.find_all('br'):
            br.decompose()
        for a in email.find_all('a'):
            a.decompose()
        return email.text.strip()
    return "Not available"


def extract_contact_info(soup):
    # Example: Assuming contact info is under a <div> with a specific class or ID
    # Adjust selector as necessary
    contact_section = soup.find('address')
    if contact_section:
        return contact_section.text.strip()
    return "Not available"


def extract_occupation(soup):
    # Example: Assuming occupation is inside a specific tag
    # Adjust selector as necessary
    occupation_section = soup.find('div', {'class': 'posts_text'})
    if occupation_section:
        return occupation_section.text.strip()
    return "Not available"


def extract_family_details(soup):
    # Find all div elements with the class posts_text
    posts_text_divs = soup.find_all('div', {'class': 'posts_text'})

    # Check if there are at least two div elements with the class posts_text
    if len(posts_text_divs) >= 2:
        # Extract the text from the second div element
        family = posts_text_divs[3]
        # Remove any unnecessary tags and text
        for br in family.find_all('br'):
            br.decompose()
        for a in family.find_all('a'):
            a.decompose()
        return family.text.strip()
    return "Not available"


def extract_political_affiliation(soup):
    # Find all div elements with the class posts_text
    posts_text_divs = soup.find_all('div', {'class': 'posts_text'})

    # Check if there are at least two div elements with the class posts_text
    if len(posts_text_divs) >= 2:
        # Extract the text from the second div element
        political_section = posts_text_divs[1]
        # Remove any unnecessary tags and text
        for br in political_section.find_all('br'):
            br.decompose()
        for a in political_section.find_all('a'):
            a.decompose()
        return political_section.text.strip()
    return "Not available"


def extract_images(soup):
    # Find the a tag with the class profile-photo
    profile_photo_tag = soup.find('a', {'class': 'profile-photo'})

    # Find the img tag inside the a tag
    if profile_photo_tag:
        img_tag = profile_photo_tag.find('img')

        # Extract the src attribute of the img tag
        if img_tag:
            return img_tag.get('src')

    return "Not available"

# Function to save details to JSON and CSV



def save_data(candidate_name, details):
    # Create a folder with the candidate's name in the output directory
    output_dir = "output"
    candidate_dir = os.path.join(output_dir, candidate_name)
    os.makedirs(candidate_dir, exist_ok=True)

    # Save to JSON
    json_file = os.path.join(candidate_dir, f"{candidate_name}.json")
    with open(json_file, 'w') as f:
        json.dump(details, f, indent=4)
    print(f"Data saved to {json_file}")

    # Save to CSV
    csv_file = os.path.join(candidate_dir, f"{candidate_name}.csv")
    with open(csv_file, mode='w') as file:
        writer = csv.DictWriter(file, fieldnames=details.keys())
        writer.writeheader()
        writer.writerow(details)
    print(f"Data saved to {csv_file}")

# Main function to run the crawler


def run_crawler(candidate_name, list_page_url):
    driver = configure_driver()

    # Step 1: Find the candidate's page
    candidate_page_url = find_candidate_page(
        driver, candidate_name, list_page_url)

    if candidate_page_url:
        # Step 2: Extract candidate details
        candidate_details = extract_candidate_details(
            driver, candidate_page_url)

        # Step 3: Save the data
        save_data(candidate_name, candidate_details)
    else:
        print("Candidate not found. Exiting.")

    driver.quit()


if __name__ == "__main__":
    candidate_name = input("Enter the candidate's name: ")
    search_url = input("Enter the search URL:\n default :https://www.pap.gov.pk/members/contactdetails/en/21?bycontact=true\n enter to continue with default")
    # Replace with the actual URL
    if not search_url:
        search_url = "https://www.pap.gov.pk/members/contactdetails/en/21?bycontact=true"
    # list_page_url = "https://www.pap.gov.pk/members/contactdetails/en/21?bycontact=true"
    run_crawler(candidate_name, search_url)
