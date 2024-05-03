import requests
import json
import csv

def send_request(resource_directory, request_url, filename):
    """
    Sends a GET request to the specified URL and saves the response data in either JSON or CSV format
    based on the content indicated by the URL parameters. It adapts the filename based on the format.

    Parameters:
    - resource_directory (str): The directory for the resource, unused in the current implementation.
    - request_url (str): The complete URL to which the GET request is sent.
    - filename (str): The base filename for saving the response, modified based on the format.
    """
    # Send the GET request to the specified URL and store the response
    response = requests.request(method="GET", url=request_url)
        
    # Check the response status and process accordingly
    if response.status_code == 200:
        # If the response contains 'format=json' in the URL, handle saving as JSON
        if 'format=json' in request_url:
            # Ensure the filename ends with '.json'
            if not filename.endswith('.json'):
                filename += '.json'
            # Open the file and save the response data as JSON
            with open(filename, "w") as file:
                parsed_json = json.loads(response.text)
                json.dump(parsed_json, file, indent=4)

        # If the response contains 'format=csv' in the URL, handle saving as CSV
        elif 'format=csv' in request_url:
            # Ensure the filename ends with '.csv'
            if not filename.endswith('.csv'):
                filename += '.csv'
            # Save as CSV
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                for line in response.text.strip().split('\n'):
                    writer.writerow(line.split(','))

        # Print the success message with the file path        
        print(f"Response saved to {filename}")
    else:
        # If the status code is not 200, print an error message with the status code
        print(f"Failed to fetch data: {response.status_code}")