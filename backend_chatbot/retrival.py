

def perform_vector_search(query_embedding):
    """
    Perform a vector search in Firestore to find the most similar document based on the embedding.

    Args:
        query_embedding (list): The embedding vector for the query.

    Returns:
        list: A list of document IDs (chunk IDs) that are the closest matches.
    """
    
    # Import necessary libraries
    from google.cloud import aiplatform, firestore
    import os
    from dotenv import load_dotenv
    import json
    from google.cloud.firestore_v1.vector import Vector
    from google.cloud.firestore_v1.base_vector_query import DistanceMeasure

    # Load environment settings
    base_directory = os.path.dirname(__file__)
    env_path = os.path.join(base_directory, '..', '.env')
    load_dotenv(dotenv_path=env_path)

    # Initialize Firestore client
    db = firestore.Client()

    # Setup for vector search in Firestore
    project_id = os.getenv('PROJECT_ID')
    region = os.getenv('LOCATION')
    embeddings_collection = db.collection('embeddings')

    # Create a Vector object from the query embedding
    query_vector = Vector(query_embedding)

    # Attempt to perform the vector search
    try:
        search_results = embeddings_collection.find_nearest(
            vector_field="embedding_field",
            query_vector=query_vector,
            distance_measure=DistanceMeasure.EUCLIDEAN,
            limit=10  # Limit of results returned can be adjusted
        )

        # Execute the query and extract chunk IDs from the results
        fetched_results = search_results.get()
        chunk_ids = [result.get('chunk_id') for result in fetched_results]
        return chunk_ids
    except Exception as e:
        print(f"An error occurred during the vector search: {str(e)}")
        return []

def retrieve_text_chunks(doc_ids):
    """
    Retrieve text chunks from Firestore given a list of document IDs.

    Args:
        doc_ids (list): List of document IDs to retrieve.

    Returns:
        list: List of text chunks associated with the given document IDs.
    """
    from google.cloud import aiplatform, firestore
    
    # Initialize Firestore client
    db = firestore.Client()
    text_chunks = []

    # Retrieve each document and extract the text
    for doc_id in doc_ids:
        doc = db.collection("text_chunks").document(doc_id).get()
        if doc.exists:
            text_chunks.append(doc.to_dict()['text'])
        else:
            print(f"Document with ID {doc_id} does not exist.")
    return text_chunks

def concatenate_texts(texts):
    """
    Concatenate a list of texts into a single string, separated by newlines.

    Args:
        texts (list): List of text strings to concatenate.

    Returns:
        str: Single concatenated string with each text separated by a newline.
    """
    return "\n".join(texts)

