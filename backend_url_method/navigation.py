from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
from sleep import sleep_random_between
import time

def navigation(driver):
    """
    Navigates to the next page in a paginated website using Selenium.

    Args:
        driver (webdriver): The Selenium WebDriver instance.

    Returns:
        tuple: A tuple containing the WebDriver instance and a boolean indicating whether there are more pages to navigate.
    """
    from selenium.common.exceptions import NoSuchElementException
    # Hardcoded XPaths based on the specific navigation bar
    next_button_xpath = "//button[@role='menuitem'][@type='button'][@tabindex='-1'][@aria-label='Go to next page'][@class='page-link']"
    no_more_pages_xpath = "//span[@role='menuitem'][@aria-label='Go to next page'][@aria-disabled='true'][@class='page-link']"
    
    try:
        # Try to find and click the 'next page' button
        next_page_button = driver.find_element(By.XPATH, next_button_xpath)
        next_page_button.click()
        print("Clicked the next page button.")
        sleep_random_between(5, 10) # Wait for 5 seconds. Consider using WebDriverWait for better practice.  # Wait for the page to load
        return driver, True
    except NoSuchElementException:
        try:
            # If the button wasn't found, check for the 'no more pages' indicator
            no_more_pages_indicator = driver.find_element(By.XPATH, no_more_pages_xpath)
            if no_more_pages_indicator:
                print("No more pages to navigate. Ending loop.")
                return driver, False
        except NoSuchElementException:
            print("Neither the button nor the end-of-pages indicator was found. Exiting.")
            return driver, False