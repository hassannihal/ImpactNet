def gemini_params(prompt, params_list):
    from dotenv import load_dotenv
    import os
    from google_auth import get_access_token
    import requests
    import json


    # Get the directory of the current script
    base_directory = os.path.dirname(__file__)
    env_path = os.path.join(base_directory, '..', '.env') # Go two levels up from the current directory
    load_dotenv(dotenv_path=env_path) # Load environment variables

    # Accessing the project ID and location from .env file
    project_id = os.getenv("PROJECT_ID")
    region = os.getenv("LOCATION")
    
    # Constructing the API URL
    api_url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/google/models/gemini-1.5-pro-preview-0409:generateContent"
    # Setting up the headers
    access_token = get_access_token()  # Call get_access_token() to dynamically obtain the token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Constructing the request body
    parameters_text = ", ".join([f"{key}: {value}" for param in params_list for key, value in param.items()])
    request_body = {
        "contents": [{
            "role": "USER",
            "parts": [
                {"text": prompt},
                {"text": parameters_text}
            ]
        }],
        "generationConfig": {
            "candidateCount": 1
        }
    }

    # Convert to JSON and send the request as before...
    json_data = request_body  # Directly use the dictionary instead of converting to string
    print(json.dumps(json_data, indent=2))
    response = requests.post(api_url, headers=headers, json=json_data)
    
    # Parsing the response
    if response.status_code == 200:
        response_json = response.json()
        #candidates = response_json.get('candidates', [])
        return response_json  # You might want to further process this to extract the exact output
        #return candidates
    else:
        return f"Error: {response.text}"


