
def catalog_apis(data):
    """
    Processes a list of data items to scrape additional details for each item from a specified catalog
    and saves all gathered data to a CSV file. The function uses Selenium and BeautifulSoup for web scraping.

    Parameters:
    - data (list of dict): List of dictionaries where each dictionary contains basic info and a URL fragment ('href').

    Returns:
    - list: A list of dictionaries containing both the original and the newly scraped data for each item.
    """
    from dotenv import load_dotenv    
    import os    
    from selenium import webdriver
    from selenium.webdriver.firefox.service import Service
    import time
    from bs4 import BeautifulSoup
    from sleep import sleep_random_between
    from navigation import navigation
    from save_to_csv import save_to_csv
    
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


    base_url = "https://data.gov.in"
    all_data_details = []
    
    # Initialize counters for managing pagination and data collection
    item_id_counter = 1
    iterations = 1
    file_number = 1
    for item in data:
        # Pause scraping every 10 iterations
        if(iterations % 10 == 0):
            sleep_random_between(100, 131)    
        details_id_counter = 1
        url = base_url + item['href'] if not item['href'].startswith(base_url) else item['href']
        driver.get(url)
        sleep_random_between(15, 35)  # Allow page to load

        # Initialize page availability for pagination
        item['item_id'] = item_id_counter
        item_id_counter += 1  # Increment the Item ID counter

        page_available = True
        while page_available:
            
            nextSoup = BeautifulSoup(driver.page_source, 'html.parser')
            cards = nextSoup.find_all(class_='card grid-box')
            for card in cards:
                # Extract details for each card
                a_tag = card.select_one('.grid-header h3 a')
                title = a_tag.text if a_tag else ''
                
                data_api_href = card.select_one('.grid-download-box .grid-download-box-inner .grid-export-box .col-md-6.col-lg-6 a')['href'] if card.select_one('.grid-download-box .grid-download-box-inner .grid-export-box .col-md-6.col-lg-6 a') else ''
                
                published_date = card.select_one('.grid-download-content .grid-download-row :-soup-contains("Published:") + strong').text if card.select_one('.grid-download-content .grid-download-row :-soup-contains("Published:") + strong') else ''
                updated_date = card.select_one('.grid-download-content .grid-download-row :-soup-contains("Updated:") + strong').text if card.select_one('.grid-download-content .grid-download-row :-soup-contains("Updated:") + strong') else ''
                
                # Copy all key-value pairs from the current item
                data_details = item.copy()
                
                # Then add or overwrite with the newly scraped details and include a unique Details ID
                data_details.update({
                    'details_id': details_id_counter,
                    'title': title,
                    'data_api_href': data_api_href,
                    'published_date': published_date,
                    'updated_date': updated_date
                })
                details_id_counter += 1  # Increment the Details ID counter
                
                all_data_details.append(data_details)
            sleep_random_between(0, 15)
            driver, page_available = navigation(driver)
    filename = 'catalogApis.csv'
    save_to_csv(all_data_details, filename)
    return all_data_details
