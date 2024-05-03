import os
import sys
from dotenv import load_dotenv
from split_pdf import split_pdf_and_upload
from gemini_request import process_image_with_api
from image_content_extractor import image_content_extractor
from process_for_vector_db import process_batches
import nltk
def setup_environment():
    """
    Load environment variables from a .env file located up two directories from the current script.
    This setup ensures that all necessary configurations are in place before processing begins.
    """
    base_directory = os.path.dirname(__file__)
    env_path = os.path.join(base_directory, '..', '.env')
    load_dotenv(dotenv_path=env_path)

def main_pdf_method(file_path, bucket_name):
    """
    Processes a PDF by splitting it and uploading the results to a specified bucket,
    then processes the uploaded content in batches.

    Args:
        file_path (str): Path to the PDF file.
        bucket_name (str): Name of the Google Cloud Storage bucket where files are uploaded.
        split (bool): Whether to split the PDF into individual pages before processing.
    """
    setup_environment()
    # Split the PDF and upload to the specified bucket
    uploaded_uris = split_pdf_and_upload(file_path, bucket_name)
    # Define the batch size for processing uploads
    batch_size = 20
    # Process the uploaded PDFs or URIs in batches    
    data = process_batches(uploaded_uris, batch_size, bucket_name)
    print("processed successfully!")
def load_text_from_file(filename):
    """
    Reads and returns the content of a text file.

    Args:
        filename (str): The path to the text file.

    Returns:
        str: The content of the file.
    """
    with open(filename, 'r') as file:
        return file.read()