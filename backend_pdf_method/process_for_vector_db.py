import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from image_content_extractor import image_content_extractor
from embed import embed_text
from google.cloud import firestore
from dotenv import load_dotenv
import uuid
import json
import tempfile
from google.cloud.firestore_v1.vector import Vector
from google.cloud import storage

# Setup and load environment
base_directory = os.path.dirname(__file__)
env_path = os.path.join(base_directory, '..', '.env')
load_dotenv(dotenv_path=env_path)
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.getenv("PROJECT_ID")
GCS_BUCKET = os.getenv('GCS_BUCKET')

# Path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

# Initialize Firestore client
db = firestore.Client()

# Ensure NLTK data is available
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
nltk_data_directory = os.path.join(parent_directory, 'nltk_data')
nltk.data.path.append(nltk_data_directory)
nltk.download('punkt', download_dir=nltk_data_directory)

def split_text_with_overlap(text, max_tokens_per_chunk, token_overlap):
    """
    Splits the provided text into chunks with a specified maximum number of tokens per chunk
    and an overlap between consecutive chunks.

    Args:
        text (str): The text to be split.
        max_tokens_per_chunk (int): Maximum number of tokens in each chunk.
        token_overlap (int): Number of tokens that overlap between consecutive chunks.

    Returns:
        list of str: Text chunks created from the input text.
    """
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    current_count = 0

    for sentence in sentences:
        tokens = word_tokenize(sentence)
        num_tokens = len(tokens)
        if current_count + num_tokens > max_tokens_per_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = tokens[:max(0, num_tokens - token_overlap)]
            current_count = num_tokens - token_overlap
        else:
            current_chunk.extend(tokens)
            current_count += num_tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks




def process_batches(image_uris, batch_size, bucket_name):
    """
    Processes batches of images, extracts text, splits the text, and saves both the text
    and its embeddings to Firestore.

    Args:
        image_uris (list of str): URIs of images to process.
        batch_size (int): Number of images to process in each batch.
        bucket_name (str): Name of the Google Cloud Storage bucket where files are uploaded.
    """    
    db = firestore.Client()
    accumulated_text = ""
    non_table_counter = 0
    chunk_size = 800
    overlap = 200

    # Process each batch of images
    for i in range(0, len(image_uris), batch_size):
        current_batch = image_uris[i:i+batch_size]
        extracted_text, table_content = image_content_extractor(current_batch)
        
        if table_content:
            process_text_and_save_embedding(extracted_text, db)
        else:
            accumulated_text += extracted_text
            non_table_counter += 1
            if non_table_counter >= 20 or i + batch_size >= len(image_uris):
                chunks = split_text_with_overlap(accumulated_text, chunk_size, overlap)
                accumulated_text = chunks.pop() if chunks else ""
                for chunk in chunks:
                    process_text_and_save_embedding(chunk, db)
                non_table_counter = 0

    if accumulated_text:
        process_text_and_save_embedding(accumulated_text, db)

def process_text_and_save_embedding(text, db):
    """
    Embeds the given text and stores both the text and its embedding in Firestore.

    Args:
        text (str): Text to embed and store.
        db (firestore.Client): Firestore client used to interact with the database.
    """    
    
    chunk_id = str(uuid.uuid4())
    embedded_chunk = embed_text(text)  # Assume this returns a list of floats representing the embedding

    # Store text chunk separately in Firestore
    db.collection('text_chunks').document(chunk_id).set({'text': text})

    # Create a Vector object from the embedding and store it with only chunk_id in Firestore
    vector_embedding = Vector(embedded_chunk)
    embedding_doc = {
        "chunk_id": chunk_id,
        "embedding_field": vector_embedding
    }
    db.collection('embeddings').add(embedding_doc)