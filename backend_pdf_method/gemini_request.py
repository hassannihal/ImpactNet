def process_image_with_api(gcs_uri, prompt):
    from dotenv import load_dotenv
    import os
    from google_auth import get_access_token
    import requests
    import json
    from process_response import process_response

    # Get the directory of the current script
    base_directory = os.path.dirname(__file__)
    env_path = os.path.join(base_directory,'..', '.env') # Go one levels up from the current directory
    load_dotenv(dotenv_path=env_path) # Load environment variables

    # Accessing the project ID and location from .env file
    project_id = os.getenv("PROJECT_ID")
    region = os.getenv("LOCATION")
    
    # Constructing the API URL to utilize appropriate model - currently set to Gemini 1.5 PRO
    api_url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/google/models/gemini-1.5-pro-preview-0409:generateContent"
    # Setting up the headers
    access_token = get_access_token()  # Call get_access_token() to obtain the token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Construct the request body using the defined text prompt
    request_body = {
        "contents": [
            {
                "role": "USER",  # Role in the conversation (here, it's the user making the request)
                "parts": [
                    {
                        # Text part using the predefined variable
                        "text": prompt
                    },
                    {
                        # File data for image file
                        "fileData": {
                            "mimeType": "image/png",
                            "fileUri": gcs_uri
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "candidateCount": 1,  # Specifies the number of response variants to generate
            #"maxOutputTokens": 200  # Limits the maximum number of tokens in the response if required
        }
    }


    # Convert to JSON and send the request as before...
    json_data = request_body
    response = requests.post(api_url, headers=headers, json=json_data)
    
    # Parsing the response
    if response.status_code == 200:
        response_json = response.json()
        # process further to extract the exact output
        return process_response(response_json)
    else:
        return f"Error: {response.text}"


