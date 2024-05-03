from google.oauth2 import service_account
from google.auth.transport.requests import Request
import os
from dotenv import load_dotenv

# Set the path to the .env file two levels up from the current script's location
base_directory = os.path.dirname(__file__)
env_path = os.path.join(base_directory, '..', '.env')
load_dotenv(dotenv_path=env_path)

def get_access_token():
    """
    Obtain an access token using a service account to authenticate API requests.

    Returns:
        str: An access token as a string that can be used in the Authorization header of API requests.
    """
    # Load the service account credentials from the environment variable
    # GOOGLE_APPLICATION_CREDENTIALS should point to the JSON key file of the service account    
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    # Request a new access token from Google
    credentials.refresh(Request())
    return credentials.token  # Return the access token