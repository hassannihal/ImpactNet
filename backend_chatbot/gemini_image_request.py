# This module handles communication with an AI platform for generating content and code based on given prompts.
# It uses environment variables for configuration and leverages a custom authentication method.

import requests
import json
import os
from dotenv import load_dotenv
from google_auth import get_access_token  # Custom module to fetch OAuth2 access token

def process_context_and_question(prompt):
    """Send a prompt to the AI platform and retrieve generated content as JSON."""
    
    base_directory = os.path.dirname(__file__)
    env_path = os.path.join(base_directory, '..', '.env')
    load_dotenv(dotenv_path=env_path)
    project_id = os.getenv("PROJECT_ID")
    region = os.getenv("LOCATION")
    api_url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/google/models/gemini-1.5-pro-preview-0409:generateContent"
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    
    request_body = {
    "contents": [{
        "role": "USER",
        "parts": [
            {
                "text": prompt  # This is the text part
            }
        ]
    }],
    "generationConfig": {
        "candidateCount": 1,
        #"responseMimeType": "application/json"
    }
}
    response = requests.post(api_url, headers=headers, json=request_body, stream=True)
    if response.status_code == 200:    
        return response.json()  # Return the full JSON response
    else:
        return {"error": f"Failed to fetch data: {response.status_code} - {response.text}"}


def process_context_and_code(prompt):
    """Send a prompt to the AI platform and retrieve generated code as JSON."""

    # Load environment and API configuration (same as in `process_context_and_question`)
    base_directory = os.path.dirname(__file__)
    env_path = os.path.join(base_directory, '..', '.env')
    load_dotenv(dotenv_path=env_path)
    project_id = os.getenv("PROJECT_ID")
    region = os.getenv("LOCATION")
    api_url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/google/models/gemini-1.5-pro-preview-0409:generateContent"
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    
    request_body = {
    "contents": [{
        "role": "USER",
        "parts": [
            {
                "text": prompt  # This is the text part
            }
        ]
    }],
    "generationConfig": {
        "candidateCount": 1,
        #"responseMimeType": "application/json"
    }
}
    response = requests.post(api_url, headers=headers, json=request_body)
    if response.status_code == 200:
        return response.json()
        #return response.json()  # Return the full JSON response
    else:
        return {"error": f"Failed to fetch data: {response.status_code} - {response.text}"}



def extract_code(data):
    """Extract data fields from response JSON, specifically targeting text and structured data within parts of a candidate."""
    text_parts = []

    # Iterate through each candidate in the response
    for candidate in data.get('candidates', []):
        content = candidate.get('content', {})
        
        # Extract data from each part of the content
        for part in content.get('parts', []):
            if 'text' in part:
                # Append text directly
                text_parts.append(part['text']) # Append text content directly
            elif 'data' in part:
                # Process structured data, e.g., labels and values for chart plotting
                if 'labels' in part['data']:
                    labels = part['data']['labels']
                    values = part['data']['values']
                    text_parts.append(f"Labels: {labels}, Values: {values}")
                else:
                    text_parts.append(json.dumps(part['data'])) # Handle generic structured data
    return ' '.join(text_parts)

