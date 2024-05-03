#gemini_api.py code:
def gemini_init():
    from google.cloud import aiplatform
    from dotenv import load_dotenv
    import os

    # Load environment variables from .env file
    base_directory = os.path.dirname(__file__)
    env_path = os.path.join(base_directory, '..', '.env')
    load_dotenv(dotenv_path=env_path)

    # Accessing the environment variables
    google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = os.getenv("PROJECT_ID")
    location = os.getenv("LOCATION")

    # Initialize the Vertex AI SDK
    aiplatform.init(project=project_id, location=location)

    # Assuming the following import and usage is correct for the SDK version you're using
    #from vertexai.preview.generative_models import GenerativeModel

    #Load the model
    #gemini_pro_model = GenerativeModel("gemini-1.0-pro")

# Generate content
#model_response = gemini_pro_model.generate_content(["What is x multiplied by 2?", "x = 42"])
#print("Model response:", model_response)

def gemini_api(prompt):
    from vertexai.preview.generative_models import GenerativeModel

    # Load the model
    #gemini_pro_model = GenerativeModel("gemini-1.0-pro")
    gemini_pro_model = GenerativeModel("gemini-1.0-pro-vision")
    num_predictions=1
    # Assuming gemini_pro_model is already initialized and available
    # Generate content based on the provided prompt
    model_response = gemini_pro_model.generate_content(prompt, num_predictions)
    return model_response
