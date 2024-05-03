#main_script.py code:
from catalog_overview import catalog_overview
from catalog_apis import catalog_apis
from extract_api import extract_api
from gemini_REST_params import gemini_params
from csv_to_list import csv_to_list
from dotenv import load_dotenv
from request_api import send_request =
import os
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.types import Integer, String, Float, Boolean
import sqlalchemy as sa
import json
from gemini_REST_schema import gemini_schema, read_json_as_text
from urllib.parse import urlencode, urljoin, urlparse, parse_qs, urlunparse
from database_import import json_to_sqlalchemy_type, create_table_from_json, load_data, process_json_files


# Set the path to the .env file one levels up
base_directory = os.path.dirname(__file__)
env_path = os.path.join(base_directory, '..', '.env')
load_dotenv(dotenv_path=env_path)

def process_url(url):
    """
    Processes a given URL to extract, transform, and load API data from an online catalog. The URL must be
    within allowed domains to initiate processing.

    Args:
    - url (str): The URL of the online catalog to process.

    Returns:
    - None: Results are saved to a file and potentially actions are logged.
    """
    allowed_domains = ['data.gov.in', 'api.data.gov.in']
    # eg: url = 'https://data.gov.in/catalogs/?ministry=Department%20of%20Higher%20Education'
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    start_process = False
    # Check if the domain of the URL is in the list of allowed domains
    if domain in allowed_domains:
        print(f"Processing URL: {url}")
        # Process the URL as required
        start_process = True
    else:
        start_process = False
        return "URL domain is not allowed"

    if(start_process == True):
        # Extract the overview data from the URL
        catalog_overview_data = catalog_overview(url)
        detailed_data = []

        # Extract detailed data from the catalog using the overview data
        detailed_data = catalog_apis(catalog_overview_data)

        # Now, detailed_data holds the comprehensive details extracted from each catalog's page
        base_url = 'https://data.gov.in'

        # Loop through each entry in the detailed data
        for entry in detailed_data:
            # Extract the data_api_href from the entry
            data_api_href = entry['data_api_href']  # ensure this key matches your CSV column name
            title = entry['title']
            # Form the full URL by appending data_api_href to base_url
            full_url = f"{base_url}{data_api_href}"
            
            # Print or use the full_url as needed
            print(full_url)

            url = full_url
            resource_directory = ''
            deterministic_flag = True # Flag to determine processing method - Deterministic code or with AI
            
            if(deterministic_flag == False): #solving using AI
                data_paths_with_parameters = extract_api(url, deterministic_flag)
                print(data_paths_with_parameters)
                for path, params_list in data_paths_with_parameters.items():
                    
                    # Construct parameter strings from each dictionary in the list
                    params_str = ', '.join([f"{key}: {value}" for param in params_list for key, value in param.items()])
                    prompt = f"""The parameters provided here along with this prompt are the parameters necessary to make a GET request to an API. Process this & create an appropriate GET request URL and return the GET request URL parameters part that need to be appended to the request endpoint within a single text output. 
                    Utilize the default value for Api key as mentioned in the api key text and the output parameter should be JSON. Just give the final output that has to be appended to request URL and no other comments or instructions from your side"""

                    # Send the prompt to Gemini AI and handle the response
                    response = gemini_params(prompt, params_list)
                    print(response)
                    resource_directory = path
                    request_params_json = ''
                    # Assuming 'response' is the data structure that contains everything
                    candidate = response['candidates'][0]  # Access the first and only candidate directly
                    part = candidate['content']['parts'][0]  # Access the first and only part directly
                    request_params_json = part['text']  # Access the text directly

                    print(request_params_json)  # Print the text
                    request_params_csv = request_params_json.replace('format=json', 'format=csv')
                    CONST_DOMAIN = 'https://api.data.gov.in'
                    request_params_csv = request_params.strip().replace('\n', '').replace(' ', '')
                    request_params_json = request_params.strip().replace('\n', '').replace(' ', '')
                    
                    request_params_csv = f"{CONST_DOMAIN}{resource_directory}{request_params_csv}"
                    request_params_json = f"{CONST_DOMAIN}{resource_directory}{request_params_json}"

            elif(deterministic_flag == True): #solving using deterministic method
                data_paths = extract_api(url, deterministic_flag)
                CONST_DOMAIN = "https://api.data.gov.in"
                api_key = os.getenv('API_KEY')
                if not api_key:
                    raise ValueError("API Key not found in the environment variables.")
                
                existing_params = {}
                existing_params['api-key'] = os.getenv('API_KEY')
                existing_params['format'] = 'csv'
                query_string = urlencode(existing_params)
                request_params_csv = f"{CONST_DOMAIN}{data_paths}?{query_string}"
                
                existing_params['format'] = 'json'
                existing_params['limit'] = 2
                query_string = urlencode(existing_params)
                request_params_json = f"{CONST_DOMAIN}{data_paths}?{query_string}"
                resource_directory = data_paths 
            filename = title
            send_request(resource_directory, request_params_json, filename)
            send_request(resource_directory, request_params_csv, filename)
     
        #Retrieve database connection details from environment variables
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASS")
        db_name = os.getenv("DB_NAME")
        db_host = os.getenv("DB_HOST")
        
        #Create the database engine
        connection_string = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
        engine = create_engine(connection_string)
        
        #Directory containing the JSON files
        directory = 'C:\\xyz\\downloads-test\\' #utilize the correct directory
        
        # Process the JSON files
        process_json_files(directory, engine)
