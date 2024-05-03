
def gemini_schema(prompt, json_text):
    import os
    import requests
    import json
    from dotenv import load_dotenv
    from google_auth import get_access_token
    
    # Get the directory of the current script
    base_directory = os.path.dirname(__file__)
    env_path = os.path.join(base_directory, '..', '.env') # Go two levels up from the current directory
    load_dotenv(dotenv_path=env_path) # Load environment variables
    
    # Accessing the project ID and location from .env file
    project_id = os.getenv("PROJECT_ID")
    region = os.getenv("LOCATION")

    # Constructing the API URL
    api_url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/google/models/gemini-1.5-pro-preview-0409:generateContent"
    
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    request_body = {
        "contents": [{
            "role": "USER",
            "parts": [
                {"text": prompt},
                {"text": json_text}
            ]
        }],
        "generationConfig": {
            "candidateCount": 1
        }
    }

    response = requests.post(api_url, headers=headers, json=request_body)
    if response.status_code == 200:
        return response.json()  # Returns the JSON response from the API
    else:
        return f"Error: {response.status_code} - {response.text}"

def read_json_as_text(json_file_path):
    import json
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
        json_text = json.dumps(json_data)
    return json_text
