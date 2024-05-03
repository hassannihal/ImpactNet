from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from sleep import sleep_random_between
from dotenv import load_dotenv    
import os 

def extract_api(url, deterministic_flag):
    """
    Extracts API details from a given URL using Selenium to interact with the page and BeautifulSoup to parse HTML.
    Optionally returns the first extracted path immediately if deterministic_flag is set.

    Args:
    - url (str): URL of the web page to extract data from.
    - deterministic_flag (bool): If set to True, returns the first data path immediately.

    Returns:
    - dict: A dictionary of data paths with their respective parameters if deterministic_flag is False.
    - str: First data path immediately if deterministic_flag is True.
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
    
    driver.get(url)
    sleep_random_between(15, 17) # Wait for JavaScript to load content

    # Initialize button click state and attempts counter   
    button_clicked = False  
    attempt = 0
    max_attempts = 3 

    # Attempt to click the button to load additional content, retry up to max_attempts times
    while not button_clicked and attempt < max_attempts:
        try:
            button = driver.find_element(By.CLASS_NAME, 'opblock-control-arrow')
            button.click()
            button_clicked = True  # Set the flag to True as the button is clicked successfully
            sleep_random_between(2, 5)  # Allow time for content to load after the click
            print("Button was successfully clicked.")
        except NoSuchElementException:
            print("Button not found, refreshing the page and trying again...")
            driver.refresh()
            sleep_random_between(15, 17)  # Wait again for JavaScript to load content after refreshing
            attempt += 1
        except Exception as e:
            print("Button click failed:", e)
            break  # Exit the loop if other exceptions occur

    # Get the page source from the driver and parse it with BeautifulSoup
    html_content = driver.page_source
    driver.quit()  
    soup = BeautifulSoup(html_content, 'html.parser')

    # Check if button was clicked and process the page content
    if(button_clicked == True):
        data_paths_with_parameters = {}
        opblocks = soup.find_all(class_='opblock-summary-path')
        for opblock in opblocks:
            data_path = opblock.get('data-path')
            if(deterministic_flag):
                return data_path
            parameters_info = []
            if data_path:
                #parameters_container = opblock.find_next_sibling(class_='parameters-container')
                parameters_container = soup.find(class_='parameters-container')
                if parameters_container:
                    table = parameters_container.find('table', class_='parameters')
                    if table:
                        tbody = table.find('tbody')
                        if tbody:
                            for row in tbody.find_all('tr'):
                            
                                # Extract the parameter's name and other details
                                name_div = row.find('div', class_='parameter__name')
                                desc_div = row.find('td', class_='parameters-col_description')
                                if name_div and desc_div:
                                    key = name_div.text.strip()
                                    value = desc_div.text.strip()
                                    # Store the key-value pair
                                    parameters_info.append({key: value})
                
                # Store the parameters associated with the path
                data_paths_with_parameters[data_path] = parameters_info
                
    # Return a dictionary of data paths with parameters if deterministic_flag is False        
    return data_paths_with_parameters