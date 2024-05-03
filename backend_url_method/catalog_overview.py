#code for finding collection of Catalog information
from dotenv import load_dotenv    
import os    
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time
from bs4 import BeautifulSoup
from sleep import sleep_random_between
from navigation import navigation
from save_to_csv import save_to_csv

def catalog_overview(url):
    """
    Scrapes catalog data from a specified URL and saves it to a CSV file. The function navigates through
    paginated content, extracts relevant catalog data, and uses Selenium along with BeautifulSoup for scraping.

    Parameters:
    - url (str): The URL of the website to scrape catalog data from.

    Returns:
    - list: A list of dictionaries containing catalog data scraped from the website.
    """
    
    # Set the path to the .env file one levels up
    base_directory = os.path.dirname(__file__)
    env_path = os.path.join(base_directory, '..', '.env')
    load_dotenv(dotenv_path=env_path)
    
    # Get the path from the environment variable
    geckodriver_path = os.getenv('GECKODRIVER_PATH')

    # Check if the environment variable was found
    if geckodriver_path is None:
        raise EnvironmentError("GECKODRIVER_PATH environment variable not set")

    # Set up the Firefox driver using the path from the environment variable
    s = Service(geckodriver_path)
    driver = webdriver.Firefox(service=s)

    # Navigate to the given URL    
    driver.get(url)
    # Wait for the content to load
    sleep_random_between(0, 5)

    # Use BeautifulSoup to parse the page source
   
    catalogData = [] # Extracting catalog information and storing it
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Initialize page availability flag for navigation    
    page_available = True
    while page_available:
        # Re-parse the page source to reflect new content after navigation
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all elements with class 'card grid-box' as they contain catalog data
        cards = soup.find_all(class_='card grid-box') 
        for card in cards:
            # Extract header and description sections from each card
            header = card.find(class_='grid-header')
            description_section = card.find(class_='grid-desc')
            descriptions = description_section.find_all(class_='card-text') if description_section else []

            # Compile all description texts into a single description string          
            desc_text = ' '.join(p.get_text(strip=True) for p in descriptions)
            
            # Check if the header section exists and process it
            if header:
                h3_tag = header.find('h3')
                if h3_tag:
                    a_tag = h3_tag.find('a')
                    if a_tag:
                        # Append the extracted data as a dictionary to catalogData list
                        catalogData.append({
                            'text': a_tag.text.strip(),
                            'href': a_tag.get('href', ''),
                            'description': desc_text
                        })
        sleep_random_between(0, 5)
        # Navigate to the next page if available
        driver, page_available = navigation(driver)
    filename = 'catalogData.csv'
    # Call the function
    save_to_csv(catalogData, filename)

    driver.quit()
    # Return the list of extracted catalog data
    return catalogData