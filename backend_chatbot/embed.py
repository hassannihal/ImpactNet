

def embed_text(text: str) -> list:
    """
    Generates a text embedding using Vertex AI's Text Embedding Model.

    Args:
        text (str): The text to be embedded.

    Returns:
        list: The embedding vector as a list of floats.
    """
    # Import necessary libraries
    import os
    from dotenv import load_dotenv  
    import vertexai
    from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

    # Set the path to the .env file two levels up and load environment variables
    base_directory = os.path.dirname(__file__)
    env_path = os.path.join(base_directory, '..', '.env')
    load_dotenv(dotenv_path=env_path)

    # Retrieve project details from environment variables
    PROJECT_ID = os.getenv('PROJECT_ID')  
    REGION = os.getenv('us-central1') # Set the appropriate region

    # Initialize Vertex AI with the specified project and region
    vertexai.init(project=PROJECT_ID, location=REGION)  

    # Configuration for the text embedding model
    model_name = "text-embedding-preview-0409"  # Specify your model
    #model_name = "textembedding-gecko@003"
    task_type = "RETRIEVAL_DOCUMENT"  # Specify your task type
    title = ""  # Optional title, can be used depending on the task
    output_dimensionality = 768  # Output dimensionality of the embeddings

    # Load the model from the specified name
    model = TextEmbeddingModel.from_pretrained(model_name)

    # Create a TextEmbeddingInput object with the given parameters
    text_embedding_input = TextEmbeddingInput(task_type=task_type, title=title, text=text)
    kwargs = {'output_dimensionality': output_dimensionality} if output_dimensionality else {}
    embeddings = model.get_embeddings([text_embedding_input], **kwargs)
    # Return the embedding values of the first (and only) text input - program is designed to process one text chunk at a time.
    return embeddings[0].values